# 🚀 Deploy to Streamlit Cloud

Quick guide to deploy the Tanzanian Rent Invoice Processor to Streamlit Cloud.

## Prerequisites

✅ GitHub repository with the code
✅ Streamlit Cloud account (free at https://streamlit.io/cloud)

## Step 1: Prepare Your Repository

Make sure your GitHub repo has these files:

### Required Files:
- ✅ `app.py` - Main application
- ✅ `requirements.txt` - Python dependencies
- ✅ `packages.txt` - System dependencies (for Tesseract & Poppler)

### Optional Files:
- `runtime.txt` - Python version specification
- `.streamlit/config.toml` - Streamlit configuration

---

## Step 2: Fix for Deployment Error

If you got the error `installer returned a non-zero exit code`, here's the fix:

### Update `requirements.txt`:

Replace the content with this **simplified version**:

```txt
streamlit
pytesseract
Pillow
pdfplumber
```

### Create `packages.txt`:

Create a new file named `packages.txt` with:

```txt
tesseract-ocr
tesseract-ocr-eng
poppler-utils
```

This file tells Streamlit Cloud to install system-level dependencies needed for OCR.

---

## Step 3: Push to GitHub

```bash
git add requirements.txt packages.txt
git commit -m "Fix: Add packages.txt for Streamlit Cloud deployment"
git push origin main
```

---

## Step 4: Deploy to Streamlit Cloud

1. **Go to**: https://share.streamlit.io/
2. **Sign in** with GitHub
3. **Click**: "New app"
4. **Fill in**:
   - **Repository**: `jmaccoe/tanzanian-rent-processor`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. **Click**: "Deploy!"

---

## Step 5: Monitor Deployment

Watch the logs for:

```
✅ Installing system dependencies from packages.txt
✅ Installing Python dependencies from requirements.txt
✅ App deployed successfully!
```

If there are errors, see the troubleshooting section below.

---

## Expected Deployment Time

- First deployment: 3-5 minutes
- Updates: 1-2 minutes

---

## Your App URL

After deployment, your app will be available at:
```
https://[your-app-name].streamlit.app
```

Example:
```
https://tanzanian-rent-processor.streamlit.app
```

---

## Troubleshooting

### Error: "No module named 'pytesseract'"

**Solution**: Ensure `packages.txt` exists with:
```
tesseract-ocr
tesseract-ocr-eng
poppler-utils
```

### Error: "installer returned a non-zero exit code"

**Solution 1**: Use simplified `requirements.txt`:
```txt
streamlit
pytesseract
Pillow
pdfplumber
```

**Solution 2**: Try `requirements-minimal.txt`:
```bash
# Rename in your repo
mv requirements-minimal.txt requirements.txt
git add requirements.txt
git commit -m "Use minimal requirements"
git push
```

### Error: "pdfplumber installation failed"

**Solution**: Explicitly add dependencies:
```txt
streamlit
pytesseract
Pillow>=10.0.0
pdfminer.six
pdfplumber
```

### Error: Python version mismatch

**Solution**: Create `runtime.txt`:
```
python-3.11
```

---

## Configuration (Optional)

### Custom Theme

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501

[browser]
gatherUsageStats = false
```

### Secrets Management

For API keys or sensitive data:

1. Go to your app settings in Streamlit Cloud
2. Click "Secrets"
3. Add as TOML format:

```toml
[TRA]
api_key = "your-key-here"

[database]
connection_string = "your-connection"
```

Access in code:
```python
import streamlit as st

api_key = st.secrets["TRA"]["api_key"]
```

---

## Post-Deployment Checklist

After successful deployment:

- ✅ Test OCR with sample invoice image
- ✅ Test PDF upload
- ✅ Test manual entry mode
- ✅ Verify calculations are correct
- ✅ Check mobile responsiveness
- ✅ Share app URL with team

---

## Update Your App

To update the app:

```bash
# Make changes to code
git add .
git commit -m "Update: description of changes"
git push origin main
```

Streamlit Cloud will automatically redeploy!

---

## Monitoring & Analytics

### View Logs

In Streamlit Cloud dashboard:
1. Click on your app
2. Click "Logs" tab
3. Monitor real-time activity

### Usage Statistics

Streamlit Cloud provides:
- Number of users
- Session duration
- Geographic distribution

---

## Cost & Limits

### Free Tier:
- ✅ Unlimited public apps
- ✅ 1GB RAM per app
- ✅ 1 CPU core per app
- ✅ Community support

### If you need more:
- Upgrade to Streamlit Cloud for Teams
- Or self-host (see DEPLOYMENT_GUIDE.md)

---

## Alternative: Self-Host

If Streamlit Cloud doesn't work, you can self-host:

### Local Network:
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Docker:
```bash
docker build -t rent-processor .
docker run -p 8501:8501 rent-processor
```

### Cloud VPS (AWS, DigitalOcean, etc.):
See DEPLOYMENT_GUIDE.md for details.

---

## Files Structure for Streamlit Cloud

Your repo should look like:

```
tanzanian-rent-processor/
├── app.py                    # Main app (required)
├── requirements.txt          # Python deps (required)
├── packages.txt              # System deps (required for OCR)
├── runtime.txt               # Python version (optional)
├── .streamlit/
│   └── config.toml          # Config (optional)
├── README.md
└── ... (other files)
```

---

## Quick Fix Summary

**Most common issue**: Missing `packages.txt`

**Quick solution**:

1. Create `packages.txt` with:
   ```
   tesseract-ocr
   tesseract-ocr-eng
   poppler-utils
   ```

2. Simplify `requirements.txt` to:
   ```
   streamlit
   pytesseract
   Pillow
   pdfplumber
   ```

3. Push to GitHub:
   ```bash
   git add packages.txt requirements.txt
   git commit -m "Fix deployment"
   git push
   ```

4. Streamlit Cloud will auto-redeploy

---

## Support

**Streamlit Cloud Issues**:
- Community Forum: https://discuss.streamlit.io/
- Documentation: https://docs.streamlit.io/streamlit-community-cloud

**App Issues**:
- Open GitHub issue in your repo
- Check INSTALL_TROUBLESHOOTING.md

---

## Success!

Once deployed, share your app:

```
🎉 Check out the Tanzanian Rent Invoice Processor!
🔗 https://[your-app].streamlit.app

Process invoices, calculate WHT, and get payment instructions instantly!
```

---

**Happy deploying!** 🚀🇹🇿
