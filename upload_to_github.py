"""
GitHub File Uploader Script
Uploads all project files to GitHub repository using GitHub API
"""

import os
import base64
import requests
from pathlib import Path

# Configuration
GITHUB_TOKEN = input("Enter your GitHub Personal Access Token: ")
REPO_OWNER = "bahyemad81"
REPO_NAME = "IDML-Test"
BRANCH = "main"
LOCAL_PATH = r"C:\Users\bahye\OneDrive\Desktop\New folder"

# Files to exclude
EXCLUDE_PATTERNS = [
    '__pycache__',
    '.git',
    'uploads',
    '.env',
    '*.idml',
    '*.docx',
    'temp_',
    '.pyc',
    'push_to_github.bat',
    'upload_to_github.py'
]

def should_exclude(file_path):
    """Check if file should be excluded"""
    path_str = str(file_path)
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str:
            return True
    return False

def upload_file(file_path, repo_path, token):
    """Upload a single file to GitHub"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{repo_path}"
    
    # Read file content
    with open(file_path, 'rb') as f:
        content = base64.b64encode(f.read()).decode('utf-8')
    
    # Prepare request
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "message": f"Add {repo_path}",
        "content": content,
        "branch": BRANCH
    }
    
    # Upload
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code in [201, 200]:
        print(f"✅ Uploaded: {repo_path}")
        return True
    else:
        print(f"❌ Failed: {repo_path} - {response.json().get('message', 'Unknown error')}")
        return False

def main():
    print("=" * 60)
    print("GitHub File Uploader")
    print("=" * 60)
    print()
    
    if not GITHUB_TOKEN or GITHUB_TOKEN == "":
        print("❌ No GitHub token provided!")
        print()
        print("To create a token:")
        print("1. Go to: https://github.com/settings/tokens")
        print("2. Click 'Generate new token (classic)'")
        print("3. Select scope: 'repo' (full control)")
        print("4. Copy the token and paste it when prompted")
        print()
        return
    
    # Get all files
    local_path = Path(LOCAL_PATH)
    files_to_upload = []
    
    for file_path in local_path.rglob('*'):
        if file_path.is_file() and not should_exclude(file_path):
            repo_path = str(file_path.relative_to(local_path)).replace('\\', '/')
            files_to_upload.append((file_path, repo_path))
    
    print(f"Found {len(files_to_upload)} files to upload")
    print()
    
    # Upload files
    success_count = 0
    fail_count = 0
    
    for file_path, repo_path in files_to_upload:
        if upload_file(file_path, repo_path, GITHUB_TOKEN):
            success_count += 1
        else:
            fail_count += 1
    
    print()
    print("=" * 60)
    print(f"✅ Successfully uploaded: {success_count} files")
    print(f"❌ Failed: {fail_count} files")
    print("=" * 60)
    print()
    print("View your repository at:")
    print(f"https://github.com/{REPO_OWNER}/{REPO_NAME}")
    print()

if __name__ == "__main__":
    main()
