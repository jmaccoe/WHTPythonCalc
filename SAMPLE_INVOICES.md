# Sample Invoice Data for Testing

This file contains sample invoice text that can be used to test the OCR parsing functionality.

## Sample 1: Basic Commercial Rent Invoice

```
AZURA BEACH CLUB LIMITED
TIN: 123-456-789

INVOICE

Invoice No: INV-2026-001
Date: 15 January 2026
Period: January 2026

Bill To:
ABC Trading Company Ltd
TIN: 987-654-321

Description: Commercial Office Rent - Main Building, Floor 3

Base Rent (excluding VAT)        TZS  5,000,000.00
VAT @ 18%                          TZS    900,000.00
                                  ___________________
TOTAL AMOUNT DUE                   TZS  5,900,000.00

Payment Details:
Payee: Azura Beach Club Limited
Bank: CRDB Bank
Account: 0150-123456-00
Branch: Kariakoo

Due Date: 31 January 2026

Thank you for your business.
```

Expected Calculations:
- Base Rent: TZS 5,000,000.00
- VAT @ 18%: TZS 900,000.00
- Total Invoice: TZS 5,900,000.00
- WHT (10% of base): TZS 500,000.00
- Pay to Landlord: TZS 5,400,000.00
- Remit to TRA: TZS 500,000.00
- Total Outflow: TZS 5,900,000.00

---

## Sample 2: Larger Amount Invoice

```
TANZANIA PROPERTIES LTD
Registered Office: Plot 123, Samora Avenue, Dar es Salaam
TIN: 111-222-333

TAX INVOICE

Invoice Number: TP-2026-002
Invoice Date: 20/01/2026
Rent Period: February 2026

Customer:
XYZ Corporation Limited
TIN: 444-555-666

Description                        Amount (TZS)
-------------------------------------------
Office Space Lease                10,000,000.00
Service Charge                     1,000,000.00
                                  --------------
Sub-total                         11,000,000.00
VAT @ 18%                          1,980,000.00
                                  --------------
TOTAL PAYABLE                     12,980,000.00

Bank Details:
Bank Name: NMB Bank PLC
Account No: 20110123456
Swift Code: NMIBTZTZ

Payment Terms: Due within 7 days
```

Expected Calculations (for Office Space only):
- Base Rent: TZS 10,000,000.00
- VAT @ 18%: TZS 1,800,000.00
- WHT (10% of base): TZS 1,000,000.00
- Pay to Landlord: TZS 10,800,000.00
- Remit to TRA: TZS 1,000,000.00

Note: Service charges may also be subject to WHT and should be handled separately.

---

## Sample 3: Small Business Invoice

```
KARIBU PLAZA MANAGEMENT
P.O. Box 12345, Mwanza
TIN: 777-888-999

RENT INVOICE

Inv#: KP/01/2026
Date: 10 Jan 2026
For: January 2026 Shop Rent

Tenant: Mama Fatma Duka
Shop No: G-15

Rent                    TSh   500,000
VAT (18%)               TSh    90,000
                        --------------
Total Due               TSh   590,000

Pay to: Karibu Plaza Management
CRDB Bank A/C: 0123456789

Thank you!
```

Expected Calculations:
- Base Rent: TZS 500,000.00
- VAT @ 18%: TZS 90,000.00
- Total Invoice: TZS 590,000.00
- WHT (10% of base): TZS 50,000.00
- Pay to Landlord: TZS 540,000.00
- Remit to TRA: TZS 50,000.00
- Total Outflow: TZS 590,000.00

---

## Sample 4: Invoice with USD Equivalent

```
INTERNATIONAL BUSINESS CENTER
Dar es Salaam, Tanzania
TIN: 100-200-300

MONTHLY RENT INVOICE

Invoice: IBC-2026-JAN-001
Date: 25 January 2026
Period: January 2026

Client: Global Tech Solutions Ltd

Description: Executive Office Suite - 5th Floor

Rent Amount                 TZS 20,000,000.00
                           (USD 8,000 approx)
VAT @ 18%                   TZS  3,600,000.00
                            ________________
TOTAL                       TZS 23,600,000.00
                           (USD 9,440 approx)

Banking Information:
Beneficiary: International Business Center Ltd
Bank: Standard Chartered Bank
Account: SCB-234567890
Branch: Samora Branch, DSM

Exchange Rate: USD 1 = TZS 2,500 (indicative)
```

Expected Calculations:
- Base Rent: TZS 20,000,000.00
- VAT @ 18%: TZS 3,600,000.00
- Total Invoice: TZS 23,600,000.00
- WHT (10% of base): TZS 2,000,000.00
- Pay to Landlord: TZS 21,600,000.00
- Remit to TRA: TZS 2,000,000.00
- Total Outflow: TZS 23,600,000.00

Note: WHT is calculated on TZS amounts, not USD.

---

## Testing Tips

1. **Creating Test Images:**
   - Type any of the above samples in a document
   - Save as PDF or take a screenshot
   - Upload to the app for testing

2. **OCR Quality:**
   - Use clear, high-contrast text
   - Avoid handwriting
   - Ensure good lighting for photos

3. **Manual Entry Testing:**
   - Use the amounts above to test manual entry
   - Verify calculations match expected results

4. **Edge Cases to Test:**
   - Very small amounts (< TZS 100,000)
   - Very large amounts (> TZS 100,000,000)
   - Round numbers vs. decimal amounts
   - Different VAT rates (if applicable)
   - Missing information scenarios
