# How to Upload Project to GitHub - Automated Script

## You Need a GitHub Personal Access Token

### Step 1: Create a Token

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Settings:
   - Note: "IDML Upload"
   - Expiration: 30 days (or your choice)
   - ✅ Check **"repo"** (full control of private repositories)
4. Click **"Generate token"**
5. **COPY THE TOKEN** (you won't see it again!)

### Step 2: Run the Upload Script

```bash
python upload_to_github.py
```

When prompted, paste your token and press Enter.

The script will upload all files to:
https://github.com/bahyemad81/IDML-Test

---

## Alternative: Manual Upload (Easier if you don't want to create a token)

1. Go to: https://github.com/bahyemad81/IDML-Test
2. Click **"Add file"** → **"Upload files"**
3. Drag all files from: `C:\Users\bahye\OneDrive\Desktop\New folder`
4. Commit message: "Initial commit"
5. Click **"Commit changes"**

✅ Done!

---

## Files That Will Be Uploaded

- ✅ streamlit_app.py
- ✅ translator_core.py
- ✅ simple_translator.py
- ✅ word_generator.py
- ✅ requirements.txt
- ✅ README.md
- ✅ All documentation files
- ✅ templates/ and static/ folders

## Files That Will Be Excluded

- ❌ __pycache__/
- ❌ uploads/
- ❌ *.idml, *.docx files
- ❌ .env file
