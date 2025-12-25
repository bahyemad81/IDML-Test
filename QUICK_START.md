# Quick Start Guide - Install Python & Run IDML Translator

## Step 1: Download Python ✅ (You're Here!)

The Python download page is now open in your browser showing **Python 3.14.2**.

**Click the download button** to get the installer.

---

## Step 2: Install Python

1. **Run the downloaded installer** (it will be in your Downloads folder)

2. **⚠️ CRITICAL**: On the first screen, **CHECK THE BOX** that says:
   ```
   ☑ Add Python to PATH
   ```
   This is essential for the application to work!

3. Click **"Install Now"**

4. Wait for installation to complete (takes 2-3 minutes)

5. Click **"Close"** when done

---

## Step 3: Verify Installation

After installation completes:

1. Open a **new** PowerShell or Command Prompt window
2. Type: `python --version`
3. You should see: `Python 3.14.2` (or similar)

If you see this, Python is installed correctly! ✅

---

## Step 4: Install Project Dependencies

In the terminal, navigate to the project folder and run:

```powershell
cd "c:\Users\bahye\OneDrive\Desktop\New folder"
python -m pip install -r requirements.txt
```

This will install:
- Flask (web server)
- OpenAI (API client)
- lxml (XML processing)
- flask-cors (CORS support)
- python-dotenv (environment variables)

Installation takes about 1-2 minutes.

---

## Step 5: Get Your OpenAI API Key

1. Visit: https://platform.openai.com/api-keys
2. Sign in to your OpenAI account
3. Click **"Create new secret key"**
4. Copy the key (starts with `sk-...`)
5. Save it somewhere safe

You can either:
- **Option A**: Enter it in the web interface when translating
- **Option B**: Create a `.env` file with: `OPENAI_API_KEY=your_key_here`

---

## Step 6: Start the Web Server

In the terminal, run:

```powershell
python app.py
```

You should see:

```
============================================================
IDML Arabic Translation Tool - Web Server
============================================================

Server starting at: http://localhost:5000

Make sure to set your OPENAI_API_KEY in .env file
or provide it through the web interface.

============================================================
 * Running on http://0.0.0.0:5000
```

---

## Step 7: Open the Web Interface

1. Open your browser
2. Navigate to: **http://localhost:5000**
3. You'll see the beautiful IDML translator interface!

---

## Step 8: Translate Your First IDML File

1. Enter your OpenAI API key in the input field
2. Drag and drop your `.idml` file (or click to browse)
3. Click **"Translate to Arabic"**
4. Wait for the translation to complete (30-60 seconds)
5. Click **"Download"** to get your translated file
6. Open the `_AR.idml` file in Adobe InDesign

---

## Troubleshooting

### "Python not found" after installation
- Did you check "Add Python to PATH"?
- Try closing and reopening your terminal
- Try using `py` instead of `python`

### "Module not found" errors
- Make sure you ran: `python -m pip install -r requirements.txt`
- Check that you're in the correct folder

### Port 5000 already in use
- Another application is using port 5000
- Edit `app.py` and change `port=5000` to `port=5001`

---

## Next Steps

**Right now**: Download and install Python from the page that's open in your browser.

**After installation**: Come back here and I'll help you run the commands to start the server!

---

**Need help?** Just ask and I'll guide you through any step! 🚀
