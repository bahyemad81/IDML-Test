# 🚀 Deploy to Streamlit Cloud - Complete Guide

Follow these steps to get your permanent FREE test link!

---

## Step 1: Install Git (if not installed)

Check if Git is installed:
```powershell
git --version
```

If not installed:
1. Download from: https://git-scm.com/download/win
2. Install with default settings
3. Restart PowerShell

---

## Step 2: Create GitHub Account

1. Go to: https://github.com/signup
2. Sign up with your email
3. Verify your email

---

## Step 3: Create GitHub Repository

1. Go to: https://github.com/new
2. Fill in:
   - **Repository name**: `idml-translation-tool`
   - **Description**: `Translate Adobe InDesign IDML files to Arabic/English`
   - **Public** ✅ (required for free Streamlit)
   - **DON'T** check "Add README" (we already have one)
3. Click **"Create repository"**

---

## Step 4: Push Code to GitHub

Open PowerShell and run these commands **one by one**:

```powershell
# Navigate to your project
cd "c:\Users\bahye\OneDrive\Desktop\New folder"

# Initialize git
git init

# Configure git (replace with YOUR info)
git config user.name "bahyemad81"
git config user.email "your-email@example.com"

# Add files
git add .

# Commit
git commit -m "Initial commit - IDML Translation Tool"

# Connect to GitHub (replace bahyemad81 with YOUR username)
git remote add origin https://github.com/bahyemad81/idml-translation-tool.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note**: When asked for password, use a **Personal Access Token**:
- Go to: https://github.com/settings/tokens
- Click "Generate new token (classic)"
- Select scopes: `repo`
- Copy token and use as password

---

## Step 5: Deploy to Streamlit Cloud

1. **Go to**: https://share.streamlit.io/
2. **Sign in** with your GitHub account
3. **Click** "New app" (top right)
4. **Fill in**:
   - **Repository**: `bahyemad81/idml-translation-tool`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
5. **Click** "Deploy!"

---

## Step 6: Wait for Deployment (2-3 minutes)

Streamlit will:
- ✅ Clone your repository
- ✅ Install dependencies from `requirements.txt`
- ✅ Start your app
- ✅ Give you a public URL

---

## Step 7: Get Your Permanent Link! 🎉

Your app will be live at:
```
https://idml-translation-tool.streamlit.app
```

Or similar URL based on your username.

**Share this link with anyone!**

---

## 🔄 Making Updates Later

When you want to update your app:

```powershell
cd "c:\Users\bahye\OneDrive\Desktop\New folder"

# Make your changes to files

# Then push:
git add .
git commit -m "Updated feature X"
git push
```

Streamlit Cloud will **auto-deploy** in 2 minutes!

---

## 🆘 Troubleshooting

### Git not found
- Install Git from https://git-scm.com/download/win
- Restart PowerShell

### Authentication failed
- Use Personal Access Token instead of password
- Get token from: https://github.com/settings/tokens

### Deployment failed
- Check `requirements.txt` has all dependencies
- Check `streamlit_app.py` has no errors
- View logs in Streamlit Cloud dashboard

---

## 📊 Monitor Your App

- **Dashboard**: https://share.streamlit.io/
- **View logs**: Click on your app → "Manage app" → "Logs"
- **Analytics**: See how many people use your tool

---

## ✅ You're Done!

Your tool is now:
- ✅ Live online
- ✅ Accessible to anyone
- ✅ Free forever
- ✅ Auto-updates from GitHub

**Share your link and enjoy!** 🎉
