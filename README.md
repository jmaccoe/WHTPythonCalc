# Tanzanian Commercial Rent Invoice Processor

A comprehensive Streamlit web application that automates Withholding Tax (WHT) calculations and payment splits for Tanzanian commercial rent invoices in compliance with TRA (Tanzania Revenue Authority) regulations.

## Features

✅ **Automatic Invoice Processing**
- Upload images (JPG, PNG) or PDFs of rent invoices
- OCR text extraction using Tesseract
- Intelligent parsing of invoice data (amounts, dates, landlord info)

✅ **Tax Calculations**
- Automatic 10% WHT calculation on gross rent (pre-VAT)
- 18% VAT verification and handling
- Payment split: Landlord vs TRA remittance
- Total outflow verification

✅ **Compliance Features**
- Step-by-step calculation breakdown
- Payment instructions for landlord and TRA
- Compliance warnings and reminders
- Record-keeping recommendations

✅ **Flexible Input**
- Upload invoice files OR manual entry
- Auto-calculation of missing values
- Error validation and correction prompts

## Tanzanian Tax Rules (2026)

This app implements current Tanzanian tax regulations:

1. **VAT (Value Added Tax)**: 18% standard rate on commercial rent
2. **WHT (Withholding Tax)**: 10% of gross rent (before VAT)
3. **Payment Structure**:
   - To Landlord: (Gross Rent - WHT) + VAT
   - To TRA: WHT amount (due within 7 days after month end)
4. **Applies to**: Resident landlords providing commercial property

### Example Calculation

```
Invoice Details:
- Base Rent: TZS 5,000,000
- VAT @ 18%: TZS 900,000
- Total Invoice: TZS 5,900,000

Calculations:
- WHT (10% of base): TZS 500,000
- Pay to Landlord: (5,000,000 - 500,000) + 900,000 = TZS 5,400,000
- Remit to TRA: TZS 500,000
- Total Outflow: TZS 5,900,000 ✓
```

## Installation

### Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **Tesseract OCR** (required for image processing)
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt-get update
   sudo apt-get install tesseract-ocr
   ```
   
   **macOS:**
   ```bash
   brew install tesseract
   ```
   
   **Windows:**
   - Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
   - Add to PATH or set TESSDATA_PREFIX environment variable

3. **Poppler** (required for PDF to image conversion)
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt-get install poppler-utils
   ```
   
   **macOS:**
   ```bash
   brew install poppler
   ```
   
   **Windows:**
   - Download from: https://github.com/oschwartz10612/poppler-windows/releases
   - Add `bin` folder to PATH

### Setup

1. **Clone or download this repository**
   ```bash
   # Create project directory
   mkdir tz-rent-processor
   cd tz-rent-processor
   ```

2. **Copy the files**
   - `app.py` (main application)
   - `requirements.txt` (dependencies)
   - `README.md` (this file)

3. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Activate on Linux/Mac:
   source venv/bin/activate
   
   # Activate on Windows:
   venv\Scripts\activate
   ```

4. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the App

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Using the App

#### Method 1: Upload Invoice File

1. Click "Upload Invoice (Image/PDF)" in the sidebar
2. Upload your invoice file (supported: JPG, PNG, PDF)
3. Review extracted information
4. Click "Calculate WHT & Payments"
5. View payment breakdown and instructions

#### Method 2: Manual Entry

1. Select "Manual Entry" in the sidebar
2. Fill in invoice details:
   - Invoice number, date, period
   - Landlord information
   - Base rent, VAT, total amounts
3. Click "Calculate WHT & Payments"
4. View results

### Understanding the Results

The app displays:

1. **Extracted Invoice Information**
   - Invoice metadata (number, date, period)
   - Landlord details (name, TIN, bank)
   - Invoice amounts with verification

2. **Tax Calculations Breakdown**
   - Step-by-step calculation
   - WHT amount (10% of base rent)
   - Payment to landlord
   - Payment to TRA
   - Total outflow verification

3. **Payment Instructions**
   - Exact amount to transfer to landlord
   - Bank details (if available)
   - WHT remittance to TRA
   - Deadlines and documentation requirements

4. **Compliance Warnings**
   - Landlord residency verification
   - TIN validation reminder
   - Record-keeping requirements
   - Professional advice recommendations

## File Structure

```
tz-rent-processor/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── venv/                 # Virtual environment (created during setup)
```

## Troubleshooting

### OCR Not Working

**Error:** "pytesseract.pytesseract.TesseractNotFoundError"

**Solution:**
1. Verify Tesseract is installed: `tesseract --version`
2. If not found, reinstall Tesseract (see Prerequisites)
3. On Windows, ensure Tesseract is in PATH or set:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

### Poor OCR Results

**Issue:** Incorrect amounts or missing data

**Solutions:**
1. Ensure invoice image is clear and high-resolution
2. Crop image to show only the invoice
3. Use PDF version if available
4. Use Manual Entry mode as fallback

### PDF Processing Fails

**Error:** "pdf2image requires poppler"

**Solution:**
1. Install Poppler (see Prerequisites)
2. On Windows, ensure Poppler's `bin` folder is in PATH

### Streamlit Port Already in Use

**Error:** "Address already in use"

**Solution:**
```bash
streamlit run app.py --server.port 8502
```

## Technical Details

### Dependencies

- **streamlit**: Web application framework
- **pytesseract**: Python wrapper for Tesseract OCR
- **Pillow (PIL)**: Image processing
- **pdfplumber**: PDF text extraction
- **pdf2image**: PDF to image conversion

### Architecture

```
User Upload
    ↓
OCR Extraction (pytesseract/pdfplumber)
    ↓
Text Parsing (regex-based)
    ↓
Data Validation
    ↓
Tax Calculations
    ↓
Results Display
```

### Tax Calculation Logic

```python
# Core calculations
WHT = Base_Rent × 0.10
Payment_to_Landlord = (Base_Rent - WHT) + VAT
Payment_to_TRA = WHT
Total_Outflow = Payment_to_Landlord + Payment_to_TRA
```

## Customization

### Adding Support for Other Languages

Edit the OCR language in `app.py`:

```python
# In OCRProcessor.extract_from_image()
text = pytesseract.image_to_string(image, lang='eng+swa')  # English + Swahili
```

### Modifying Tax Rates

Update the constants in `TaxCalculator` class:

```python
class TaxCalculator:
    WHT_RATE = Decimal("0.10")  # Change WHT rate here
    VAT_RATE_STANDARD = Decimal("0.18")  # Change VAT rate here
```

### Adding Additional Fields

Extend the `InvoiceData` class and update parsing logic:

```python
class InvoiceData:
    def __init__(self):
        # Add new fields
        self.service_charge: Optional[Decimal] = None
        self.maintenance_fee: Optional[Decimal] = None
```

## Legal & Compliance

⚠️ **Important Disclaimers:**

1. **Not Official TRA Software**: This tool is independent and not affiliated with Tanzania Revenue Authority
2. **Information Purposes Only**: Calculations are based on publicly available tax information as of January 2026
3. **Professional Advice Required**: Always consult qualified tax professionals for:
   - Complex transactions
   - Large amounts
   - Non-standard situations
   - Verification of residency status
   - Tax planning
4. **No Guarantee**: While we strive for accuracy, users are responsible for verifying all calculations
5. **Tax Law Changes**: Tax rates and rules may change. Stay updated via TRA official channels

## Support & Resources

### Official Resources

- **TRA Website**: https://www.tra.go.tz
- **TRA Online Services**: https://www.tra.go.tz/index.php/online-services
- **VAT Information**: https://www.tra.go.tz/index.php/vat
- **Income Tax**: https://www.tra.go.tz/index.php/income-tax

### Getting Help

For technical issues with this app:
1. Check the Troubleshooting section
2. Verify all prerequisites are installed
3. Review error messages carefully

For tax compliance questions:
1. Contact TRA directly
2. Consult a registered tax advisor
3. Review TRA published guidelines

## Version History

### Version 1.0 (January 2026)
- Initial release
- Image and PDF upload support
- Automatic OCR extraction
- Manual entry option
- WHT and VAT calculations
- Payment instructions
- Compliance warnings

## Future Enhancements

Planned features:
- [ ] Bulk invoice processing
- [ ] Export to Excel/CSV
- [ ] Integration with accounting software
- [ ] Historical records database
- [ ] Multi-language support (Swahili)
- [ ] TIN verification API integration
- [ ] PDF report generation
- [ ] Service charge calculations
- [ ] Multiple payment method support

## License

This software is provided as-is for educational and business use. Users are responsible for compliance with all applicable tax laws and regulations.

## Contributing

Suggestions and improvements welcome! For major changes:
1. Test thoroughly with sample invoices
2. Verify calculations match TRA requirements
3. Document any tax rule changes

---

**Made with ❤️ for Tanzanian businesses**

*Last Updated: January 2026*
