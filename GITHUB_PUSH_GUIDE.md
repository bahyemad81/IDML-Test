# Push to GitHub - Setup Guide

## Your Repository
**GitHub URL:** https://github.com/bahyemad81/IDML-Test

## Option 1: Using GitHub Desktop (Easiest)

### Step 1: Install GitHub Desktop
1. Download from: https://desktop.github.com/
2. Install and sign in with your GitHub account

### Step 2: Add Your Project
1. Open GitHub Desktop
2. Click **File** → **Add Local Repository**
3. Browse to: `C:\Users\bahye\OneDrive\Desktop\New folder`
4. Click **Add Repository**
5. If it says "not a Git repository", click **Create a repository**

### Step 3: Make Initial Commit
1. You'll see all your files in the "Changes" tab
2. In the bottom left:
   - Summary: `Initial commit - IDML Arabic Translation Tool`
   - Description: `Added complete translation tool with Streamlit UI`
3. Click **Commit to main**

### Step 4: Publish to GitHub
1. Click **Publish repository** (top right)
2. Repository name: `IDML-Test`
3. **UNCHECK** "Keep this code private" (if you want it public)
4. Click **Publish Repository**

✅ **Done!** Your code is now on GitHub at https://github.com/bahyemad81/IDML-Test

---

## Option 2: Using Git Command Line

### Step 1: Install Git
1. Download from: https://git-scm.com/download/win
2. Run installer (use default settings)
3. Restart your terminal/PowerShell

### Step 2: Configure Git (First Time Only)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Initialize and Push
```bash
# Navigate to your project
cd "C:\Users\bahye\OneDrive\Desktop\New folder"

# Initialize Git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit - IDML Arabic Translation Tool"

# Add remote repository
git remote add origin https://github.com/bahyemad81/IDML-Test.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: Enter Credentials
When prompted, enter your GitHub username and **Personal Access Token** (not password).

**To create a token:**
1. Go to: https://github.com/settings/tokens
2. Click **Generate new token (classic)**
3. Select scopes: `repo` (full control)
4. Copy the token and use it as your password

---

## What's Included in Your Repository

### Core Files
- `streamlit_app.py` - Streamlit web interface
- `translator_core.py` - Translation engine
- `simple_translator.py` - Google Translate integration
- `word_generator.py` - Word document generator
- `requirements.txt` - Python dependencies

### Documentation
- `README.md` - Main project documentation
- `QUICK_START.md` - Quick start guide
- `SETUP_INSTRUCTIONS.md` - Setup instructions
- `DEPLOYMENT.md` - Deployment guide
- `ARABIC_FIX_GUIDE.md` - Arabic rendering fixes
- `ARABIC_FIX_SUMMARY.md` - Summary of Arabic fixes
- `ARABIC_TROUBLESHOOTING.md` - Troubleshooting guide

### Configuration
- `.gitignore` - Git ignore rules (excludes uploads, temp files, etc.)
- `requirements.txt` - Python dependencies

---

## Next Steps After Pushing

### Deploy to Streamlit Cloud (Free Hosting)

1. Go to: https://share.streamlit.io
2. Sign in with GitHub
3. Click **New app**
4. Select:
   - Repository: `bahyemad81/IDML-Test`
   - Branch: `main`
   - Main file: `streamlit_app.py`
5. Click **Deploy**

You'll get a public URL like: `https://idml-test.streamlit.app`

This URL can be shared with anyone! 🎉

---

## Troubleshooting

### "Repository already exists"
If the repository already has content:
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### "Authentication failed"
- Use a **Personal Access Token** instead of your password
- Create one at: https://github.com/settings/tokens

### "Permission denied"
- Make sure you're logged into the correct GitHub account
- Check that you have write access to the repository
