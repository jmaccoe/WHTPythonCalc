# Quick Start Guide

Get up and running with the Tanzanian Rent Invoice Processor in 5 minutes!

## 🚀 Super Quick Start (For Ubuntu/Debian)

```bash
# 1. Install system dependencies
sudo apt-get update
sudo apt-get install -y tesseract-ocr poppler-utils python3-pip

# 2. Install Python packages
pip install streamlit pytesseract Pillow pdfplumber pdf2image

# 3. Run the app
streamlit run app.py
```

Your browser will open automatically at http://localhost:8501

## 🚀 Super Quick Start (For macOS)

```bash
# 1. Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install system dependencies
brew install tesseract poppler python

# 3. Install Python packages
pip3 install streamlit pytesseract Pillow pdfplumber pdf2image

# 4. Run the app
streamlit run app.py
```

## 🚀 Super Quick Start (For Windows)

```powershell
# 1. Install Tesseract OCR
# Download and install from: https://github.com/UB-Mannheim/tesseract/wiki
# During installation, note the installation path (usually C:\Program Files\Tesseract-OCR)

# 2. Install Poppler
# Download from: https://github.com/oschwartz10612/poppler-windows/releases
# Extract to C:\poppler
# Add C:\poppler\Library\bin to your PATH

# 3. Install Python packages
pip install streamlit pytesseract Pillow pdfplumber pdf2image

# 4. Run the app
streamlit run app.py
```

## 📱 First Time Usage

### Option A: Upload an Invoice

1. Open the app at http://localhost:8501
2. Click "Choose a file" under "Upload Invoice"
3. Select your invoice (JPG, PNG, or PDF)
4. Review extracted information
5. Click "Calculate WHT & Payments"
6. View results and payment instructions

### Option B: Manual Entry

1. Select "Manual Entry" from the sidebar
2. Fill in the form:
   - Invoice details (number, date, period)
   - Landlord information
   - **Required**: Base Rent, VAT Amount, Total
3. Click "Calculate WHT & Payments"
4. Get your results instantly!

## 🧪 Test the App

Run the test script to verify calculations:

```bash
python test_calculations.py
```

You should see:
```
ALL TESTS PASSED! ✅
```

## 📊 Example Calculation

Let's say your invoice shows:
- Base Rent: **TZS 5,000,000**
- VAT @ 18%: **TZS 900,000**
- Total: **TZS 5,900,000**

The app will calculate:

✅ **Transfer to Landlord: TZS 5,400,000**
   - (5,000,000 - 500,000) + 900,000

✅ **Remit to TRA: TZS 500,000**
   - 10% WHT on base rent

✅ **Total Outflow: TZS 5,900,000**
   - Matches your invoice ✓

## 🔍 Troubleshooting Quick Fixes

### "Tesseract not found"
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Windows: Reinstall Tesseract and add to PATH
```

### "pdf2image error"
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler

# Windows: Download Poppler, extract, and add bin folder to PATH
```

### "Port 8501 already in use"
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

### OCR gives wrong results
1. Use a clearer image/PDF
2. Crop to just the invoice
3. Use Manual Entry mode instead

## 📚 Next Steps

Once the app is running:

1. **Read the full README.md** for detailed information
2. **Check SAMPLE_INVOICES.md** for test data
3. **Customize settings** in the sidebar
4. **Bookmark the app** for regular use

## ⚖️ Legal Reminder

⚠️ This tool is for calculation assistance only. Always:
- Verify calculations independently
- Consult with TRA for compliance questions
- Keep proper documentation
- Use qualified tax advisors for large transactions

## 🆘 Need Help?

**Technical Issues:**
- Check prerequisites are installed: `tesseract --version` and `python --version`
- Review error messages carefully
- Try manual entry if OCR fails

**Tax Questions:**
- Contact TRA: https://www.tra.go.tz
- Consult registered tax advisor
- Review TRA guidelines

---

## 🎯 Common Use Cases

### Case 1: Monthly Office Rent
1. Get invoice from landlord
2. Upload to app
3. Transfer calculated amount to landlord
4. Remit WHT to TRA by 7th of next month
5. File monthly WHT return

### Case 2: New Lease Agreement
1. Review lease terms
2. Input first month's rent details
3. Set up standing payment instructions
4. Schedule monthly WHT remittances

### Case 3: Rent Review
1. Upload new invoice with increased rent
2. Calculate new WHT obligations
3. Update payment instructions
4. Inform accounting department

---

**You're all set! 🎉**

Open your browser to http://localhost:8501 and start processing invoices!
