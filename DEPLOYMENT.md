# IDML Translation Tool - Deployment Guide

## 🚀 Deploy to Streamlit Cloud (FREE)

### Step 1: Prepare Your Code

1. **Create a GitHub repository**
   - Go to https://github.com/new
   - Name it: `idml-translation-tool`
   - Make it public
   - Don't initialize with README

2. **Push your code to GitHub**
   ```bash
   cd "c:\Users\bahye\OneDrive\Desktop\New folder"
   git init
   git add streamlit_app.py translator_core.py simple_translator.py word_generator.py requirements.txt
   git commit -m "Initial commit - IDML Translation Tool"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/idml-translation-tool.git
   git push -u origin main
   ```

### Step 2: Deploy to Streamlit Cloud

1. **Go to** https://streamlit.io/cloud
2. **Sign in** with your GitHub account
3. **Click** "New app"
4. **Select** your repository: `idml-translation-tool`
5. **Main file path**: `streamlit_app.py`
6. **Click** "Deploy!"

### Step 3: Your App is Live! 🎉

- **URL**: `https://YOUR_USERNAME-idml-translation-tool.streamlit.app`
- **Share** this URL with anyone
- **Updates**: Push to GitHub → Auto-deploys

---

## 🔧 Making Changes

1. **Edit** `streamlit_app.py` locally
2. **Test** with `streamlit run streamlit_app.py`
3. **Commit** changes:
   ```bash
   git add .
   git commit -m "Updated feature X"
   git push
   ```
4. **Streamlit Cloud** auto-deploys in ~2 minutes

---

## 📊 Features

- ✅ **FREE** hosting (unlimited)
- ✅ **Auto-deploy** from GitHub
- ✅ **HTTPS** included
- ✅ **Custom domain** (optional)
- ✅ **Analytics** (view usage stats)

---

## 🌐 Alternative: Deploy to Render.com

If you prefer Render.com:

1. Go to https://render.com
2. Connect GitHub repo
3. Create new "Web Service"
4. Build command: `pip install -r requirements.txt`
5. Start command: `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`

---

## 💡 Tips

- **Monitor usage**: Check Streamlit Cloud dashboard
- **Add secrets**: Use Streamlit secrets for API keys
- **Custom domain**: Available on paid plans ($20/month)
- **Analytics**: Track how many people use your tool

---

## 🆘 Need Help?

- Streamlit Docs: https://docs.streamlit.io
- Community Forum: https://discuss.streamlit.io
- GitHub Issues: Create in your repo
