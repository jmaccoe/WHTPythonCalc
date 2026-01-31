# 🚀 GitHub Setup Instructions

Complete step-by-step guide to push this app to GitHub: http://github.com/jmaccoe/

## Prerequisites

✅ Git installed on your computer
✅ GitHub account (jmaccoe)
✅ All project files downloaded

## Step-by-Step Instructions

### Step 1: Download All Files

Make sure you have downloaded all these files to a folder on your computer:

```
tanzanian-rent-processor/
├── app.py
├── requirements.txt
├── test_calculations.py
├── config.ini
├── README.md
├── QUICKSTART.md
├── SAMPLE_INVOICES.md
├── DEPLOYMENT_GUIDE.md
├── CONTRIBUTING.md
├── LICENSE
├── .gitignore
└── GITHUB_SETUP.md (this file)
```

### Step 2: Create GitHub Repository

**Option A: Via GitHub Website**

1. Go to https://github.com/jmaccoe
2. Click the green "New" button (or go to https://github.com/new)
3. Fill in:
   - **Repository name**: `tanzanian-rent-processor` (or your preferred name)
   - **Description**: `Streamlit app for processing Tanzanian commercial rent invoices with automatic WHT calculations`
   - **Public** or **Private**: Choose based on your preference
   - **Do NOT** initialize with README, .gitignore, or license (we have these already)
4. Click "Create repository"

**Option B: Via GitHub CLI** (if you have it installed)

```bash
gh repo create tanzanian-rent-processor --public --description "Streamlit app for Tanzanian rent invoice WHT calculations"
```

### Step 3: Initialize Git Repository Locally

Open terminal/command prompt and navigate to your project folder:

```bash
# Navigate to your project folder
cd path/to/tanzanian-rent-processor

# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Tanzanian rent invoice processor with WHT calculations"
```

### Step 4: Connect to GitHub

Replace `jmaccoe` and `tanzanian-rent-processor` with your actual username and repo name:

```bash
# Add GitHub repository as remote
git remote add origin https://github.com/jmaccoe/tanzanian-rent-processor.git

# Verify remote was added
git remote -v
```

You should see:
```
origin  https://github.com/jmaccoe/tanzanian-rent-processor.git (fetch)
origin  https://github.com/jmaccoe/tanzanian-rent-processor.git (push)
```

### Step 5: Push to GitHub

```bash
# Push to GitHub (main branch)
git branch -M main
git push -u origin main
```

**If prompted for credentials:**
- **Username**: `jmaccoe`
- **Password**: Use a Personal Access Token (NOT your GitHub password)
  - Create token at: https://github.com/settings/tokens
  - Select scopes: `repo` (full control of private repositories)
  - Copy the token and paste as password

### Step 6: Verify Upload

1. Go to https://github.com/jmaccoe/tanzanian-rent-processor
2. You should see all your files
3. The README.md will display automatically on the repository page

## Alternative: Using GitHub Desktop

If you prefer a GUI:

1. **Download GitHub Desktop**: https://desktop.github.com/
2. **Install and sign in** with your GitHub account
3. **Add local repository**:
   - File → Add Local Repository
   - Choose your project folder
4. **Publish to GitHub**:
   - Click "Publish repository"
   - Set name: `tanzanian-rent-processor`
   - Choose Public/Private
   - Click "Publish Repository"

## After Pushing to GitHub

### Add Topics/Tags

On your GitHub repository page:

1. Click the gear icon ⚙️ next to "About"
2. Add topics:
   - `tanzania`
   - `tax-calculator`
   - `streamlit`
   - `withholding-tax`
   - `invoice-processing`
   - `ocr`
   - `python`
   - `accounting`

### Enable GitHub Pages (Optional)

If you want to host documentation:

1. Go to Settings → Pages
2. Source: Deploy from branch `main`
3. Folder: `/docs` (if you create a docs folder)
4. Click Save

### Add Repository Description

On the main page, click "Edit" next to the description and add:
```
🏢 Streamlit web app for processing Tanzanian commercial rent invoices with automatic Withholding Tax (WHT) calculations. Compliant with TRA regulations. Features OCR, PDF processing, and detailed payment instructions.
```

### Set Up Branch Protection (Recommended)

Settings → Branches → Add rule:
- Branch name pattern: `main`
- ✅ Require pull request reviews before merging
- ✅ Require status checks to pass

## Making Future Updates

When you make changes to the code:

```bash
# Check what changed
git status

# Stage changes
git add .

# Or stage specific files
git add app.py requirements.txt

# Commit with descriptive message
git commit -m "Fix: Correct VAT calculation for edge cases"

# Push to GitHub
git push origin main
```

## Creating Releases

When you have a stable version:

1. **Tag the version**:
   ```bash
   git tag -a v1.0.0 -m "Version 1.0.0: Initial release"
   git push origin v1.0.0
   ```

2. **Create GitHub Release**:
   - Go to your repo → Releases → "Create a new release"
   - Choose tag: `v1.0.0`
   - Release title: `v1.0.0 - Initial Release`
   - Description: List features and changes
   - Click "Publish release"

## Repository Structure

Your GitHub repo will look like this:

```
jmaccoe/tanzanian-rent-processor/
│
├── 📄 README.md                    ← Main documentation (shows on repo page)
├── 📄 LICENSE                       ← MIT License
├── 📄 .gitignore                    ← Git ignore rules
│
├── 🚀 QUICKSTART.md                 ← Quick setup guide
├── 📚 DEPLOYMENT_GUIDE.md           ← Deployment instructions
├── 📝 SAMPLE_INVOICES.md            ← Test data
├── 🤝 CONTRIBUTING.md               ← Contribution guidelines
│
├── 🐍 app.py                        ← Main Streamlit application
├── 📋 requirements.txt              ← Python dependencies
├── 🧪 test_calculations.py          ← Test suite
└── ⚙️ config.ini                    ← Configuration file
```

## Sharing Your Repository

Share with others:
```
https://github.com/jmaccoe/tanzanian-rent-processor
```

Clone instructions for others:
```bash
git clone https://github.com/jmaccoe/tanzanian-rent-processor.git
cd tanzanian-rent-processor
pip install -r requirements.txt
streamlit run app.py
```

## Troubleshooting

### "Permission denied (publickey)"

Use HTTPS instead of SSH:
```bash
git remote set-url origin https://github.com/jmaccoe/tanzanian-rent-processor.git
```

### "Repository not found"

1. Verify repository exists: https://github.com/jmaccoe/tanzanian-rent-processor
2. Check your GitHub username
3. Ensure you have access to the repository

### "Failed to push some refs"

```bash
# Pull first, then push
git pull origin main --rebase
git push origin main
```

### Authentication Failed

1. Don't use your GitHub password
2. Create Personal Access Token:
   - Go to https://github.com/settings/tokens
   - Generate new token (classic)
   - Select `repo` scope
   - Use token as password when prompted

## Next Steps

After pushing to GitHub:

1. ✅ Star your own repo (why not! 😄)
2. ✅ Share with colleagues
3. ✅ Add issues for planned features
4. ✅ Set up GitHub Actions for testing (advanced)
5. ✅ Create a project board for task tracking

## Need Help?

- 📖 GitHub Docs: https://docs.github.com/
- 💬 GitHub Community: https://github.community/
- 📧 Git help: `git --help`

---

## Quick Command Reference

```bash
# Check status
git status

# Add files
git add .

# Commit
git commit -m "Your message"

# Push
git push origin main

# Pull latest
git pull origin main

# View history
git log --oneline

# Create branch
git checkout -b feature-name

# Switch branch
git checkout main

# View remotes
git remote -v
```

---

**You're all set to push to GitHub!** 🎉

Start with Step 1 and follow through Step 5. If you encounter any issues, check the Troubleshooting section.

Good luck! 🚀
