# 🔧 Installation Troubleshooting Guide

## Common Installation Errors and Solutions

### Error: "installer returned a non-zero exit code"

This error occurs when pip cannot install dependencies. Here are solutions:

---

## Solution 1: Use Minimal Requirements (Recommended First)

Instead of `requirements.txt`, use `requirements-minimal.txt`:

```bash
pip install -r requirements-minimal.txt
```

This installs the latest compatible versions without version locks.

---

## Solution 2: Install Dependencies One by One

```bash
pip install streamlit
pip install pytesseract
pip install Pillow
pip install pdfplumber
pip install pdf2image
```

This helps identify which package is causing issues.

---

## Solution 3: Use Virtual Environment (Best Practice)

### Python 3.8-3.11:

```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install packages
pip install --upgrade pip
pip install -r requirements.txt
```

### Python 3.12+ (externally-managed-environment error):

```bash
# Use --break-system-packages (Ubuntu/Debian)
pip install -r requirements.txt --break-system-packages

# OR create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Solution 4: Platform-Specific Fixes

### Ubuntu/Debian

```bash
# Update system first
sudo apt update
sudo apt upgrade

# Install Python development headers
sudo apt install python3-dev python3-pip

# Install system packages for dependencies
sudo apt install tesseract-ocr poppler-utils

# Then install Python packages
pip install -r requirements.txt --break-system-packages
```

### macOS

```bash
# Update Homebrew
brew update

# Install dependencies
brew install python tesseract poppler

# Install Python packages
pip3 install -r requirements.txt
```

### Windows

```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install packages
pip install -r requirements.txt
```

---

## Solution 5: Streamlit Cloud Deployment

If deploying to Streamlit Cloud and getting this error:

### Option A: Simplify requirements.txt

Replace the entire `requirements.txt` with:

```
streamlit
pytesseract
Pillow
pdfplumber
```

### Option B: Add packages.txt for system dependencies

Create a file named `packages.txt` (alongside requirements.txt):

```
tesseract-ocr
poppler-utils
```

This tells Streamlit Cloud to install system-level dependencies.

---

## Solution 6: Specific Package Issues

### If Pillow fails:

```bash
# Ubuntu/Debian
sudo apt install python3-pil python3-pillow

# macOS
brew install libjpeg libpng

# Then
pip install Pillow --no-cache-dir
```

### If pdfplumber fails:

```bash
pip install pycryptodome
pip install pdfplumber
```

### If pytesseract fails:

```bash
# Install Tesseract first
# Ubuntu: sudo apt install tesseract-ocr
# macOS: brew install tesseract
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki

# Then
pip install pytesseract
```

---

## Solution 7: Check Python Version

```bash
python --version
```

**Required**: Python 3.8 or higher

If you have an older version:

```bash
# Ubuntu/Debian
sudo apt install python3.11

# macOS
brew install python@3.11

# Windows
Download from https://www.python.org/downloads/
```

---

## Solution 8: Clean Install

```bash
# Remove existing virtual environment
rm -rf venv

# Clear pip cache
pip cache purge

# Upgrade pip
pip install --upgrade pip

# Create fresh virtual environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install fresh
pip install streamlit pytesseract Pillow pdfplumber
```

---

## Solution 9: Offline/Air-gapped Installation

If you have no internet on deployment server:

```bash
# On machine with internet, download packages
pip download -r requirements.txt -d ./packages

# Copy ./packages folder to deployment server

# On deployment server
pip install --no-index --find-links=./packages -r requirements.txt
```

---

## Solution 10: Use Conda (Alternative)

```bash
# Create conda environment
conda create -n rent-processor python=3.11
conda activate rent-processor

# Install packages
conda install -c conda-forge streamlit pillow
pip install pytesseract pdfplumber pdf2image
```

---

## Verification

After installation, verify all packages are installed:

```python
python -c "import streamlit; import pytesseract; import PIL; import pdfplumber; print('✅ All packages imported successfully!')"
```

---

## Still Having Issues?

### Check for conflicts:

```bash
pip check
```

### View installed versions:

```bash
pip list | grep -E "streamlit|pytesseract|Pillow|pdfplumber"
```

### Get detailed error:

```bash
pip install -r requirements.txt --verbose
```

---

## Quick Test Commands

Test each component:

```bash
# Test Streamlit
streamlit version

# Test Tesseract
tesseract --version

# Test Python imports
python -c "import streamlit; print('Streamlit OK')"
python -c "import pytesseract; print('Pytesseract OK')"
python -c "import PIL; print('Pillow OK')"
python -c "import pdfplumber; print('PDFPlumber OK')"
```

---

## For Deployment Platforms

### Streamlit Cloud
- Use `requirements-minimal.txt`
- Add `packages.txt` with system dependencies
- Ensure Python version in `.streamlit/config.toml`

### Heroku
- Add `runtime.txt` with: `python-3.11.x`
- Use `Procfile`: `web: streamlit run app.py --server.port=$PORT`

### Docker
```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["streamlit", "run", "app.py"]
```

### AWS/Azure/GCP
- Use virtual environment
- Install system dependencies first
- Use requirements-minimal.txt for flexibility

---

## Last Resort: Manual Package Versions

If all else fails, create a `requirements-locked.txt`:

```
streamlit==1.40.0
pytesseract==0.3.13
Pillow==11.0.0
pdfplumber==0.11.4
pdf2image==1.17.0
```

Find compatible versions at: https://pypi.org/

---

## Get Help

If none of these work:

1. Run: `pip install -r requirements.txt --verbose > error.log 2>&1`
2. Share error.log in GitHub issues
3. Include:
   - OS and version
   - Python version
   - Error message
   - What you've tried

---

**Pro Tip**: Always use a virtual environment to avoid system conflicts!

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
