"""
Tanzanian Commercial Rent Invoice Processor
Automatically calculates withholding tax (WHT) and payment splits for commercial rent invoices.

Tax Rules (Tanzania 2026):
- Commercial rent is subject to 18% VAT (standard rate)
- Tenant withholds 10% income tax on GROSS rent (before VAT)
- WHT applies only to base rent, NOT to VAT
- Payment split: (Base rent - WHT) + VAT to landlord, WHT to TRA
"""

import streamlit as st
import re
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Optional, Tuple
import io
from PIL import Image
import pytesseract
import pdfplumber
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="TZ Rent Invoice Processor",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
        color: #1f77b4;
    }
    .warning-box {
        padding: 20px;
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        border-radius: 5px;
        margin: 10px 0;
    }
    .success-box {
        padding: 20px;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        border-radius: 5px;
        margin: 10px 0;
    }
    .info-box {
        padding: 20px;
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        border-radius: 5px;
        margin: 10px 0;
    }
    .calculation-table {
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)


class InvoiceData:
    """Data class to hold parsed invoice information"""
    def __init__(self):
        self.invoice_number: Optional[str] = None
        self.invoice_date: Optional[str] = None
        self.rent_period: Optional[str] = None
        self.description: Optional[str] = None
        self.base_rent_tzs: Optional[Decimal] = None
        self.vat_rate: Optional[Decimal] = None
        self.vat_amount_tzs: Optional[Decimal] = None
        self.total_amount_tzs: Optional[Decimal] = None
        self.landlord_name: Optional[str] = None
        self.landlord_tin: Optional[str] = None
        self.landlord_bank: Optional[str] = None
        self.landlord_account: Optional[str] = None
        self.usd_equivalent: Optional[str] = None
        self.raw_text: str = ""


class TaxCalculator:
    """Handles all tax calculations for Tanzanian commercial rent"""
    
    WHT_RATE = Decimal("0.10")  # 10% withholding tax
    VAT_RATE_STANDARD = Decimal("0.18")  # 18% standard VAT rate
    
    @staticmethod
    def calculate_wht(gross_rent: Decimal) -> Decimal:
        """Calculate 10% WHT on gross rent (before VAT)"""
        return (gross_rent * TaxCalculator.WHT_RATE).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    
    @staticmethod
    def calculate_payment_to_landlord(
        gross_rent: Decimal, 
        vat_amount: Decimal, 
        wht: Decimal
    ) -> Decimal:
        """Calculate net payment to landlord: (Gross Rent - WHT) + VAT"""
        return ((gross_rent - wht) + vat_amount).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    
    @staticmethod
    def calculate_total_outflow(payment_to_landlord: Decimal, wht: Decimal) -> Decimal:
        """Calculate total tenant outflow"""
        return (payment_to_landlord + wht).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    
    @staticmethod
    def verify_vat_rate(vat_amount: Decimal, base_amount: Decimal) -> Tuple[Decimal, bool]:
        """Verify and calculate effective VAT rate"""
        if base_amount == 0:
            return Decimal("0"), False
        
        effective_rate = (vat_amount / base_amount).quantize(
            Decimal("0.0001"), rounding=ROUND_HALF_UP
        )
        
        # Check if rate is close to 18%
        is_standard = abs(effective_rate - TaxCalculator.VAT_RATE_STANDARD) < Decimal("0.01")
        
        return effective_rate, is_standard


class OCRProcessor:
    """Handles OCR extraction from images and PDFs"""
    
    @staticmethod
    def extract_from_image(image: Image.Image) -> str:
        """Extract text from image using Tesseract OCR"""
        try:
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Use pytesseract to extract text
            text = pytesseract.image_to_string(image, lang='eng')
            return text
        except Exception as e:
            st.error(f"OCR Error: {str(e)}")
            return ""
    
    @staticmethod
    def extract_from_pdf(pdf_file) -> str:
        """Extract text from PDF using pdfplumber"""
        try:
            text = ""
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
            return text
        except Exception as e:
            st.error(f"PDF Extraction Error: {str(e)}")
            return ""


class InvoiceParser:
    """Parses invoice text to extract relevant information"""
    
    @staticmethod
    def parse_invoice(raw_text: str) -> InvoiceData:
        """Parse invoice text and extract key information"""
        invoice = InvoiceData()
        invoice.raw_text = raw_text
        
        # Extract invoice number
        inv_num_patterns = [
            r'Invoice\s*(?:No|Number|#)[:\s]*([A-Z0-9\-/]+)',
            r'INV[:\s]*([A-Z0-9\-/]+)',
        ]
        for pattern in inv_num_patterns:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                invoice.invoice_number = match.group(1).strip()
                break
        
        # Extract dates
        date_patterns = [
            r'Date[:\s]*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
            r'(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})',
        ]
        for pattern in date_patterns:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                invoice.invoice_date = match.group(1).strip()
                break
        
        # Extract rent period
        period_patterns = [
            r'(?:Period|Month|For)[:\s]*([A-Za-z]+\s+\d{4})',
            r'Rent\s+for[:\s]*([A-Za-z]+\s+\d{4})',
        ]
        for pattern in period_patterns:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                invoice.rent_period = match.group(1).strip()
                break
        
        # Extract description
        desc_patterns = [
            r'Description[:\s]*([^\n]+)',
            r'(?:Office|Shop|Commercial)\s+(?:Rent|Lease)[^\n]*',
        ]
        for pattern in desc_patterns:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                invoice.description = match.group(0).strip()
                break
        
        # Extract amounts (TZS)
        amount_patterns = [
            r'(?:TZS|TSh|Tsh)\s*([0-9,]+(?:\.\d{2})?)',
            r'([0-9,]+(?:\.\d{2})?)\s*(?:TZS|TSh)',
        ]
        
        amounts = []
        for pattern in amount_patterns:
            matches = re.finditer(pattern, raw_text, re.IGNORECASE)
            for match in matches:
                amount_str = match.group(1).replace(',', '')
                try:
                    amounts.append(Decimal(amount_str))
                except:
                    continue
        
        # Extract VAT information
        vat_patterns = [
            r'VAT\s*(?:@\s*)?(\d+)%[:\s]*(?:TZS|TSh)?\s*([0-9,]+(?:\.\d{2})?)',
            r'(?:TZS|TSh)?\s*([0-9,]+(?:\.\d{2})?)\s*VAT',
        ]
        for pattern in vat_patterns:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    invoice.vat_rate = Decimal(match.group(1)) / 100
                    invoice.vat_amount_tzs = Decimal(match.group(2).replace(',', ''))
                else:
                    invoice.vat_amount_tzs = Decimal(match.group(1).replace(',', ''))
                break
        
        # Try to identify base rent, VAT, and total from amounts
        if len(amounts) >= 2:
            # Assume last amount is total, second to last might be VAT
            invoice.total_amount_tzs = amounts[-1]
            
            if invoice.vat_amount_tzs is None and len(amounts) >= 3:
                invoice.vat_amount_tzs = amounts[-2]
            
            # Calculate base rent if we have total and VAT
            if invoice.total_amount_tzs and invoice.vat_amount_tzs:
                invoice.base_rent_tzs = invoice.total_amount_tzs - invoice.vat_amount_tzs
        
        # Extract landlord information
        landlord_patterns = [
            r'(?:Payee|Landlord|Company)[:\s]*([^\n]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Ltd|Limited|Company|Co\.))',
        ]
        for pattern in landlord_patterns:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                invoice.landlord_name = match.group(1).strip()
                break
        
        # Extract TIN
        tin_patterns = [
            r'TIN[:\s]*(\d{9,10})',
            r'Tax\s+ID[:\s]*(\d{9,10})',
        ]
        for pattern in tin_patterns:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                invoice.landlord_tin = match.group(1).strip()
                break
        
        # Extract bank details
        bank_patterns = [
            r'Bank[:\s]*([^\n]+)',
            r'Account[:\s]*([0-9\-]+)',
        ]
        for i, pattern in enumerate(bank_patterns):
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                if i == 0:
                    invoice.landlord_bank = match.group(1).strip()
                else:
                    invoice.landlord_account = match.group(1).strip()
        
        # Extract USD equivalent if present
        usd_pattern = r'USD\s*([0-9,]+(?:\.\d{2})?)'
        match = re.search(usd_pattern, raw_text, re.IGNORECASE)
        if match:
            invoice.usd_equivalent = match.group(0).strip()
        
        return invoice
    
    @staticmethod
    def validate_invoice(invoice: InvoiceData) -> Tuple[bool, list]:
        """Validate that required fields are present"""
        errors = []
        
        if not invoice.base_rent_tzs or invoice.base_rent_tzs <= 0:
            errors.append("Base rent amount is missing or invalid")
        
        if not invoice.vat_amount_tzs or invoice.vat_amount_tzs < 0:
            errors.append("VAT amount is missing or invalid")
        
        if not invoice.total_amount_tzs or invoice.total_amount_tzs <= 0:
            errors.append("Total amount is missing or invalid")
        
        # Check if amounts are consistent
        if invoice.base_rent_tzs and invoice.vat_amount_tzs and invoice.total_amount_tzs:
            expected_total = invoice.base_rent_tzs + invoice.vat_amount_tzs
            if abs(expected_total - invoice.total_amount_tzs) > Decimal("0.10"):
                errors.append(
                    f"Amount mismatch: Base ({invoice.base_rent_tzs:,.2f}) + "
                    f"VAT ({invoice.vat_amount_tzs:,.2f}) ≠ "
                    f"Total ({invoice.total_amount_tzs:,.2f})"
                )
        
        return len(errors) == 0, errors


def format_currency(amount: Decimal, currency: str = "TZS") -> str:
    """Format currency with proper thousand separators"""
    return f"{currency} {amount:,.2f}"


def display_header():
    """Display app header"""
    st.markdown('<p class="big-font">🏢 Tanzanian Commercial Rent Invoice Processor</p>', 
                unsafe_allow_html=True)
    st.markdown("""
    This tool automatically calculates **Withholding Tax (WHT)** obligations and payment splits 
    for Tanzanian commercial rent invoices in compliance with TRA regulations.
    """)
    
    with st.expander("ℹ️ How it works (Tanzania Tax Rules 2026)"):
        st.markdown("""
        **Tax Treatment for Commercial Rent:**
        
        1. **VAT (Value Added Tax):** 18% standard rate on commercial rent
        2. **WHT (Withholding Tax):** 10% of gross rent (before VAT) - withheld by tenant
        3. **Payment Split:**
           - To Landlord: (Gross Rent - WHT) + VAT
           - To TRA: WHT amount (remit within 7 days after month end)
        
        **Example:**
        - Base Rent: TZS 5,000,000
        - VAT @ 18%: TZS 900,000
        - Total Invoice: TZS 5,900,000
        
        **Calculations:**
        - WHT (10% of base): TZS 500,000
        - Pay to Landlord: (5,000,000 - 500,000) + 900,000 = **TZS 5,400,000**
        - Remit to TRA: **TZS 500,000**
        - Total Outflow: TZS 5,900,000 ✓
        """)


def manual_input_form() -> Optional[InvoiceData]:
    """Display manual input form for invoice data"""
    st.subheader("📝 Manual Invoice Entry")
    
    invoice = InvoiceData()
    
    col1, col2 = st.columns(2)
    
    with col1:
        invoice.invoice_number = st.text_input("Invoice Number")
        invoice.invoice_date = st.text_input("Invoice Date")
        invoice.rent_period = st.text_input("Rent Period (e.g., January 2026)")
        invoice.description = st.text_input("Description", value="Commercial Office Rent")
        
    with col2:
        invoice.landlord_name = st.text_input("Landlord/Payee Name")
        invoice.landlord_tin = st.text_input("Landlord TIN (optional)")
        invoice.landlord_bank = st.text_input("Bank Name (optional)")
        invoice.landlord_account = st.text_input("Account Number (optional)")
    
    st.markdown("---")
    st.markdown("**💰 Invoice Amounts (in TZS)**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        base_rent = st.number_input(
            "Base Rent (excluding VAT)",
            min_value=0.0,
            value=0.0,
            step=100000.0,
            format="%.2f"
        )
        invoice.base_rent_tzs = Decimal(str(base_rent)) if base_rent > 0 else None
    
    with col2:
        vat_amount = st.number_input(
            "VAT Amount",
            min_value=0.0,
            value=0.0,
            step=10000.0,
            format="%.2f"
        )
        invoice.vat_amount_tzs = Decimal(str(vat_amount)) if vat_amount > 0 else None
    
    with col3:
        total_amount = st.number_input(
            "Total Invoice Amount",
            min_value=0.0,
            value=0.0,
            step=100000.0,
            format="%.2f"
        )
        invoice.total_amount_tzs = Decimal(str(total_amount)) if total_amount > 0 else None
    
    # Auto-calculate missing values
    if invoice.base_rent_tzs and invoice.vat_amount_tzs and not invoice.total_amount_tzs:
        invoice.total_amount_tzs = invoice.base_rent_tzs + invoice.vat_amount_tzs
        st.info(f"Auto-calculated Total: {format_currency(invoice.total_amount_tzs)}")
    
    if invoice.base_rent_tzs and invoice.total_amount_tzs and not invoice.vat_amount_tzs:
        invoice.vat_amount_tzs = invoice.total_amount_tzs - invoice.base_rent_tzs
        st.info(f"Auto-calculated VAT: {format_currency(invoice.vat_amount_tzs)}")
    
    if st.button("Calculate WHT & Payments", type="primary"):
        is_valid, errors = InvoiceParser.validate_invoice(invoice)
        if is_valid:
            return invoice
        else:
            for error in errors:
                st.error(f"❌ {error}")
            return None
    
    return None


def display_extracted_data(invoice: InvoiceData):
    """Display extracted invoice data"""
    st.subheader("📄 Extracted Invoice Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Invoice Details:**")
        if invoice.invoice_number:
            st.write(f"• Invoice No: {invoice.invoice_number}")
        if invoice.invoice_date:
            st.write(f"• Date: {invoice.invoice_date}")
        if invoice.rent_period:
            st.write(f"• Period: {invoice.rent_period}")
        if invoice.description:
            st.write(f"• Description: {invoice.description}")
    
    with col2:
        st.markdown("**Landlord Information:**")
        if invoice.landlord_name:
            st.write(f"• Name: {invoice.landlord_name}")
        if invoice.landlord_tin:
            st.write(f"• TIN: {invoice.landlord_tin}")
        if invoice.landlord_bank:
            st.write(f"• Bank: {invoice.landlord_bank}")
        if invoice.landlord_account:
            st.write(f"• Account: {invoice.landlord_account}")
    
    st.markdown("---")
    st.markdown("**💰 Invoice Amounts:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if invoice.base_rent_tzs:
            st.metric("Base Rent", format_currency(invoice.base_rent_tzs))
    
    with col2:
        if invoice.vat_amount_tzs:
            st.metric("VAT Amount", format_currency(invoice.vat_amount_tzs))
            
            if invoice.base_rent_tzs:
                effective_rate, is_standard = TaxCalculator.verify_vat_rate(
                    invoice.vat_amount_tzs, 
                    invoice.base_rent_tzs
                )
                rate_display = f"{effective_rate * 100:.1f}%"
                if not is_standard:
                    st.warning(f"⚠️ VAT rate appears to be {rate_display}, not standard 18%")
                else:
                    st.caption(f"✓ VAT @ {rate_display}")
    
    with col3:
        if invoice.total_amount_tzs:
            st.metric("Total Invoice", format_currency(invoice.total_amount_tzs))
    
    if invoice.usd_equivalent:
        st.info(f"💵 USD Equivalent noted: {invoice.usd_equivalent}")


def calculate_and_display_taxes(invoice: InvoiceData):
    """Calculate and display tax breakdown"""
    st.subheader("🧮 Tax Calculations & Payment Breakdown")
    
    # Calculate WHT
    wht_amount = TaxCalculator.calculate_wht(invoice.base_rent_tzs)
    
    # Calculate payment to landlord
    payment_to_landlord = TaxCalculator.calculate_payment_to_landlord(
        invoice.base_rent_tzs,
        invoice.vat_amount_tzs,
        wht_amount
    )
    
    # Calculate total outflow
    total_outflow = TaxCalculator.calculate_total_outflow(payment_to_landlord, wht_amount)
    
    # Display calculation breakdown
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("**Step-by-Step Calculation:**")
    st.markdown(f"""
    1. **Gross Rent (Base):** {format_currency(invoice.base_rent_tzs)}
    2. **VAT @ 18%:** {format_currency(invoice.vat_amount_tzs)}
    3. **Withholding Tax (10% of Base):** {format_currency(wht_amount)}
    4. **Net Rent to Landlord:** {format_currency(invoice.base_rent_tzs)} - {format_currency(wht_amount)} = {format_currency(invoice.base_rent_tzs - wht_amount)}
    5. **Total to Landlord:** {format_currency(invoice.base_rent_tzs - wht_amount)} + {format_currency(invoice.vat_amount_tzs)} = {format_currency(payment_to_landlord)}
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display payment summary in metrics
    st.markdown("---")
    st.markdown("### 💳 Payment Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Transfer to Landlord",
            format_currency(payment_to_landlord),
            help="Net rent + VAT amount"
        )
    
    with col2:
        st.metric(
            "Remit to TRA (WHT)",
            format_currency(wht_amount),
            help="10% withholding tax on base rent"
        )
    
    with col3:
        st.metric(
            "Total Cash Outflow",
            format_currency(total_outflow),
            delta=f"Matches invoice: {format_currency(invoice.total_amount_tzs)}" 
                  if abs(total_outflow - invoice.total_amount_tzs) < Decimal("0.10") 
                  else "⚠️ Mismatch!"
        )
    
    # Verification
    if abs(total_outflow - invoice.total_amount_tzs) > Decimal("0.10"):
        st.error(f"⚠️ **Verification Failed:** Total outflow ({format_currency(total_outflow)}) "
                f"does not match invoice total ({format_currency(invoice.total_amount_tzs)}). "
                f"Please verify the input amounts.")
    else:
        st.success("✅ **Verification Passed:** Total outflow matches invoice total")
    
    return payment_to_landlord, wht_amount, total_outflow


def display_payment_instructions(invoice: InvoiceData, payment_to_landlord: Decimal, wht_amount: Decimal):
    """Display detailed payment instructions"""
    st.markdown("---")
    st.subheader("📋 Payment Instructions")
    
    # Payment to Landlord
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.markdown("### 1️⃣ Transfer to Landlord")
    st.markdown(f"""
    **Amount:** {format_currency(payment_to_landlord)}
    
    **Payee Details:**
    - Name: {invoice.landlord_name or "As per invoice"}
    {f"- TIN: {invoice.landlord_tin}" if invoice.landlord_tin else ""}
    {f"- Bank: {invoice.landlord_bank}" if invoice.landlord_bank else ""}
    {f"- Account: {invoice.landlord_account}" if invoice.landlord_account else ""}
    
    **Reference:** {invoice.invoice_number or "Invoice payment"} - {invoice.rent_period or "Rent payment"}
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Payment to TRA
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.markdown("### 2️⃣ Remit WHT to TRA")
    st.markdown(f"""
    **Amount:** {format_currency(wht_amount)}
    
    **Payment Method:**
    - Use TRA's online portal or authorized bank
    - Payment Type: Withholding Tax on Rent
    - Tax Code: Typically use Income Tax code for rent WHT
    
    **Deadline:** Within 7 days after the end of the month
    
    **Documentation:**
    - Obtain WHT certificate from TRA system
    - Keep proof of payment for your records
    - Provide WHT certificate to landlord for their tax filing
    """)
    st.markdown('</div>', unsafe_allow_html=True)


def display_compliance_warnings():
    """Display compliance warnings and reminders"""
    st.markdown("---")
    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.markdown("### ⚠️ Important Compliance Reminders")
    st.markdown("""
    1. **Landlord Residency:** This calculation assumes a **resident landlord**. Non-resident landlords 
       may have different WHT rates. Verify landlord's tax residency status.
    
    2. **TIN Validation:** Always verify the landlord's TIN with TRA to ensure they're properly registered.
    
    3. **Service Charges:** If the invoice includes service charges (cleaning, security, etc.), these may 
       also be subject to 10% WHT as separate items.
    
    4. **VAT Registration:** Confirm the landlord is VAT-registered and the VAT shown is legitimate. 
       Request VAT certificate if needed.
    
    5. **WHT Certificate:** After remitting WHT to TRA, obtain and provide the WHT certificate to the 
       landlord within the required timeframe.
    
    6. **Record Keeping:** Maintain copies of:
       - Original invoice
       - Bank transfer receipts
       - TRA payment confirmation
       - WHT certificates
    
    7. **Monthly Returns:** Remember to file your monthly WHT return with TRA, declaring all rent payments.
    
    8. **Professional Advice:** This tool provides calculations only. For complex situations or large 
       amounts, consult a qualified tax accountant or advisor.
    
    9. **Residential vs Commercial:** These rules apply to **commercial** rent only. Residential rent 
       has different tax treatment in Tanzania.
    
    10. **Exchange Rates:** If invoice shows USD equivalent, use TRA's official exchange rate for the 
        transaction date if you need to report in foreign currency.
    """)
    st.markdown('</div>', unsafe_allow_html=True)


def main():
    """Main application function"""
    display_header()
    
    # Sidebar for options
    with st.sidebar:
        st.markdown("### 🔧 Options")
        
        input_method = st.radio(
            "Choose input method:",
            ["Upload Invoice (Image/PDF)", "Manual Entry"],
            help="Upload an invoice file or enter details manually"
        )
        
        st.markdown("---")
        st.markdown("### 📚 Resources")
        st.markdown("""
        - [TRA Official Website](https://www.tra.go.tz)
        - [VAT Act Tanzania](https://www.tra.go.tz/index.php/vat)
        - [Income Tax Act](https://www.tra.go.tz/index.php/income-tax)
        """)
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        **Version:** 1.0  
        **Last Updated:** January 2026
        
        This tool is for informational purposes only. 
        Always verify with TRA or your tax advisor.
        """)
    
    # Main content area
    if input_method == "Upload Invoice (Image/PDF)":
        st.markdown("---")
        st.subheader("📤 Upload Invoice")
        
        uploaded_file = st.file_uploader(
            "Choose an invoice file (Image: JPG, PNG | PDF)",
            type=['jpg', 'jpeg', 'png', 'pdf'],
            help="Upload a clear image or PDF of your commercial rent invoice"
        )
        
        if uploaded_file is not None:
            # Display uploaded file
            file_type = uploaded_file.type
            
            with st.spinner("Processing invoice..."):
                # Extract text based on file type
                if file_type.startswith('image'):
                    # Image file
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Uploaded Invoice", use_container_width=True)
                    
                    with st.expander("🔍 View OCR Extracted Text"):
                        raw_text = OCRProcessor.extract_from_image(image)
                        st.text_area("Raw Text", raw_text, height=200)
                    
                elif file_type == 'application/pdf':
                    # PDF file
                    st.success("PDF uploaded successfully")
                    
                    with st.expander("🔍 View Extracted Text"):
                        raw_text = OCRProcessor.extract_from_pdf(uploaded_file)
                        st.text_area("Raw Text", raw_text, height=200)
                else:
                    st.error("Unsupported file type")
                    return
                
                # Parse the extracted text
                if raw_text.strip():
                    invoice = InvoiceParser.parse_invoice(raw_text)
                    
                    # Validate extraction
                    is_valid, errors = InvoiceParser.validate_invoice(invoice)
                    
                    if not is_valid:
                        st.warning("⚠️ Could not extract all required information automatically. "
                                 "Please review and correct below:")
                        for error in errors:
                            st.error(f"• {error}")
                        
                        # Show manual correction form
                        st.markdown("---")
                        invoice = manual_input_form()
                        if invoice:
                            display_extracted_data(invoice)
                            payment_to_landlord, wht_amount, total_outflow = calculate_and_display_taxes(invoice)
                            display_payment_instructions(invoice, payment_to_landlord, wht_amount)
                            display_compliance_warnings()
                    else:
                        # Successfully extracted
                        st.success("✅ Invoice data extracted successfully!")
                        display_extracted_data(invoice)
                        
                        if st.button("Calculate WHT & Payments", type="primary"):
                            payment_to_landlord, wht_amount, total_outflow = calculate_and_display_taxes(invoice)
                            display_payment_instructions(invoice, payment_to_landlord, wht_amount)
                            display_compliance_warnings()
                else:
                    st.error("❌ Could not extract text from the file. Please try manual entry or upload a clearer image.")
    
    else:  # Manual Entry
        st.markdown("---")
        invoice = manual_input_form()
        
        if invoice:
            st.markdown("---")
            display_extracted_data(invoice)
            payment_to_landlord, wht_amount, total_outflow = calculate_and_display_taxes(invoice)
            display_payment_instructions(invoice, payment_to_landlord, wht_amount)
            display_compliance_warnings()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p><strong>Disclaimer:</strong> This tool provides tax calculations based on Tanzanian tax law as of January 2026. 
        Tax laws may change. Always consult with TRA or a qualified tax professional for compliance verification.</p>
        <p>Made with ❤️ for Tanzanian businesses | Not affiliated with TRA</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
