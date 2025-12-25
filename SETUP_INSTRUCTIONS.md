# IDML Arabic Translation Tool - Setup Instructions

## ⚠️ Python Not Found

Python is not currently installed on your system. To run this web application, you need to install Python first.

## Quick Setup Guide

### Step 1: Install Python

1. **Download Python 3.11 or higher**:
   - Visit: https://www.python.org/downloads/
   - Download the latest Python 3.11+ installer for Windows

2. **Run the installer**:
   - ✅ **IMPORTANT**: Check "Add Python to PATH" during installation
   - Click "Install Now"

3. **Verify installation**:
   - Open a new Command Prompt or PowerShell window
   - Run: `python --version`
   - You should see: `Python 3.11.x` or higher

### Step 2: Install Dependencies

Open a terminal in this project folder and run:

```bash
python -m pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- OpenAI (API client)
- lxml (XML processing)
- flask-cors (CORS support)
- python-dotenv (environment variables)

### Step 3: Configure API Key (Optional)

You can either:

**Option A**: Create a `.env` file in this folder:
```
OPENAI_API_KEY=your_api_key_here
```

**Option B**: Enter your API key through the web interface when translating

### Step 4: Start the Server

Run:
```bash
python app.py
```

You should see:
```
============================================================
IDML Arabic Translation Tool - Web Server
============================================================

Server starting at: http://localhost:5000
...
============================================================
```

### Step 5: Open the Web Interface

1. Open your browser
2. Navigate to: `http://localhost:5000`
3. Upload an IDML file and translate!

## Alternative: Use Pre-built Executable (Coming Soon)

If you don't want to install Python, we can create a standalone executable using PyInstaller. Let me know if you'd like me to create that version.

## Troubleshooting

### "Python not found" after installation
- Make sure you checked "Add Python to PATH" during installation
- Restart your terminal/PowerShell
- Try using `py` instead of `python`

### Port 5000 already in use
- Edit `app.py` and change the port number in the last line
- Or stop the application using port 5000

### Module not found errors
- Make sure you ran `pip install -r requirements.txt`
- Try: `python -m pip install --upgrade -r requirements.txt`

## Need Help?

If you encounter any issues, please let me know and I can help troubleshoot!

---

**Ready to translate?** Follow the steps above and you'll be up and running in minutes! 🚀
