# How to Restart Your Streamlit App

## The Problem

You're seeing Arabic text even when translating to English because the Streamlit app is running the **old version** of the code (before the bidirectional fix).

## The Solution: Restart Streamlit

### Method 1: Stop and Restart (Recommended)

1. **Find the terminal/PowerShell window** where Streamlit is running
2. **Press `Ctrl+C`** to stop the app
3. **Run again:**
   ```bash
   streamlit run streamlit_app.py
   ```
4. **Refresh your browser** or go to http://localhost:8501

### Method 2: Use Streamlit's Auto-Reload

1. **In your browser**, look for the menu (☰) in the top right
2. Click **"Rerun"** or press `R`
3. This should reload the code

### Method 3: Kill and Restart

If the app is stuck:

```powershell
# Find and kill Streamlit process
taskkill /F /IM streamlit.exe

# Or find Python processes running Streamlit
Get-Process python | Where-Object {$_.MainWindowTitle -like "*Streamlit*"} | Stop-Process -Force

# Then restart
streamlit run streamlit_app.py
```

---

## Verify It's Working

After restarting:

1. **Upload an Arabic IDML file**
2. **Select "English" as target language**
3. **Click "Translate Now"**
4. **Download the file**
5. **Open in InDesign**

You should see:
- ✅ Text in ENGLISH (not Arabic!)
- ✅ Left-to-right direction
- ✅ Properly connected letters

---

## What Changed

The updated code now:
- Detects target language (`ar` or `en`)
- Applies correct formatting:
  - **English:** LTR + standard composer + English language ID
  - **Arabic:** RTL + World-Ready composer + Arabic language ID
- Actually translates the text (not just formatting!)

---

## Still Not Working?

If you still see Arabic after restarting:

1. **Check you selected "English"** in the dropdown (not Arabic)
2. **Verify the file uploaded** - make sure it's an Arabic file
3. **Check the terminal** for any error messages
4. **Try translating a simple test:**
   - Run: `python test_translator_file.py`
   - Check: `translation_test_results.txt`
   - Should show successful translations

---

## Quick Test Command

```bash
# Stop current app
Ctrl+C

# Restart
streamlit run streamlit_app.py
```

Then try translating again!
