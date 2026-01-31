# 🏢 Tanzanian Commercial Rent Invoice Processor

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> 🇹🇿 Automated Withholding Tax (WHT) calculator and payment processor for Tanzanian commercial rent invoices, compliant with TRA regulations (2026).

![App Screenshot Placeholder](https://via.placeholder.com/800x400/1f77b4/ffffff?text=Streamlit+Invoice+Processor)

## 🌟 Features

- **📤 Multiple Input Methods**
  - Upload invoice images (JPG/PNG) with OCR
  - Upload PDF invoices with text extraction
  - Manual entry with auto-calculation
  
- **🧮 Accurate Tax Calculations**
  - 10% WHT on base rent (pre-VAT)
  - 18% VAT verification
  - Payment splits: Landlord vs TRA
  - Decimal precision handling
  
- **✅ Compliance Features**
  - Step-by-step calculation breakdown
  - Payment instructions with deadlines
  - TRA regulation warnings
  - Record-keeping recommendations

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/jmaccoe/tanzanian-rent-processor.git
cd tanzanian-rent-processor

# Install system dependencies (Ubuntu/Debian)
sudo apt-get install tesseract-ocr poppler-utils

# Install Python packages
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

App opens at `http://localhost:8501`

### macOS

```bash
brew install tesseract poppler
pip3 install -r requirements.txt
streamlit run app.py
```

See [QUICKSTART.md](QUICKSTART.md) for detailed installation on all platforms.

## 💡 How It Works

### Tanzanian Tax Rules (2026)

```
Commercial Rent Invoice:
├─ Base Rent: TZS 5,000,000
├─ VAT @ 18%: TZS 900,000
└─ Total: TZS 5,900,000

Tax Calculations:
├─ WHT (10% of base): TZS 500,000
├─ To Landlord: TZS 5,400,000
│   └─ (5,000,000 - 500,000) + 900,000
├─ To TRA: TZS 500,000
└─ Total Outflow: TZS 5,900,000 ✓
```

### Processing Flow

```mermaid
graph LR
    A[Upload Invoice] --> B[OCR/Text Extract]
    B --> C[Parse Data]
    C --> D[Validate]
    D --> E[Calculate WHT]
    E --> F[Display Results]
```

## 📊 Usage Example

### Option 1: Upload Invoice

1. Take photo of rent invoice
2. Upload to app
3. Review extracted data
4. Get payment breakdown

### Option 2: Manual Entry

```python
# Example input
Base Rent: 5,000,000 TZS
VAT: 900,000 TZS
Total: 5,900,000 TZS

# Output
✅ Transfer to Landlord: 5,400,000 TZS
✅ Remit to TRA: 500,000 TZS
```

## 🧪 Testing

```bash
# Run automated tests
python test_calculations.py
```

All tests passing ✅

## 📁 Project Structure

```
tanzanian-rent-processor/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── test_calculations.py      # Automated test suite
├── config.ini               # Configuration settings
├── README.md                # This file
├── QUICKSTART.md            # Quick setup guide
├── DEPLOYMENT_GUIDE.md      # Deployment instructions
├── SAMPLE_INVOICES.md       # Test data
├── CONTRIBUTING.md          # Contribution guidelines
└── LICENSE                  # MIT License
```

## 🔧 Configuration

Edit `config.ini` to customize:

```ini
[TAX_RATES]
WHT_RATE = 0.10              # 10% withholding tax
VAT_RATE_STANDARD = 0.18     # 18% VAT

[COMPLIANCE]
WHT_REMITTANCE_DAYS = 7      # Deadline after month end
```

## 📚 Documentation

- [📖 Full Documentation](README.md)
- [🚀 Quick Start Guide](QUICKSTART.md)
- [📋 Deployment Guide](DEPLOYMENT_GUIDE.md)
- [📝 Sample Invoices](SAMPLE_INVOICES.md)
- [🤝 Contributing](CONTRIBUTING.md)

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **OCR**: Tesseract, pytesseract
- **PDF**: pdfplumber, pdf2image
- **Image**: Pillow (PIL)
- **Language**: Python 3.8+

## ⚖️ Legal & Compliance

⚠️ **Disclaimer**: This tool provides calculations for informational purposes only. It does not constitute legal or tax advice.

**Important**:
- Always verify calculations independently
- Consult TRA for official compliance guidance
- Use qualified tax professionals for large transactions
- Keep proper documentation

**Tax Law References**:
- TRA Website: https://www.tra.go.tz
- VAT Act: 18% standard rate
- Income Tax Act: 10% WHT on commercial rent

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Areas for contribution:
- 🐛 Bug fixes
- 📚 TRA regulation updates
- 🧪 Additional test cases
- 🌍 Swahili translation
- 📊 Export features (PDF, Excel)

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- Built for Tanzanian businesses
- Tax rules per TRA regulations (January 2026)
- Not affiliated with Tanzania Revenue Authority

## 📞 Support

- 📖 [Documentation](README.md)
- 🐛 [Report Issues](https://github.com/jmaccoe/tanzanian-rent-processor/issues)
- 💬 [Discussions](https://github.com/jmaccoe/tanzanian-rent-processor/discussions)

## 🗺️ Roadmap

- [ ] Batch invoice processing
- [ ] Excel/CSV export
- [ ] Invoice history database
- [ ] Swahili language support
- [ ] Mobile app version
- [ ] API integration
- [ ] Cloud deployment guide

## 📈 Version History

### v1.0.0 (January 2026)
- ✅ Initial release
- ✅ Image/PDF upload with OCR
- ✅ Manual entry mode
- ✅ WHT & VAT calculations
- ✅ Payment instructions
- ✅ Compliance warnings

---

<div align="center">

**Made with ❤️ for Tanzanian businesses**

[⭐ Star this repo](https://github.com/jmaccoe/tanzanian-rent-processor) | [🐛 Report Bug](https://github.com/jmaccoe/tanzanian-rent-processor/issues) | [💡 Request Feature](https://github.com/jmaccoe/tanzanian-rent-processor/issues)

</div>
