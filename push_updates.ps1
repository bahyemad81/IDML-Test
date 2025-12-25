# Quick Update Script for Live App

# Navigate to project
cd "c:\Users\bahye\OneDrive\Desktop\New folder"

# Add GitHub remote (replace with your actual repo URL)
# Find your repo URL at: https://share.streamlit.io/ -> Click your app -> "Manage app" -> "Settings"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Add all files
git add .

# Commit
git commit -m "Updated translation features and fixes"

# Push to GitHub
git branch -M main
git push -u origin main

# Streamlit will auto-deploy in 2-3 minutes!
