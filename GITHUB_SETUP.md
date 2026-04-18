## 🚀 GitHub Push Setup Instructions

### Step 1: Install Git for Windows
Since Git is not installed on your system, please:

**Option A: Manual Installation**
1. Download from: https://git-scm.com/download/win
2. Run the installer (.exe file)
3. Use default settings or customize as needed
4. Click "Install"

**Option B: Using Chocolatey (if installed)**
```powershell
choco install git -y
```

**Option C: Using winget with Admin Privileges**
```powershell
# Run PowerShell as Administrator first, then:
winget install --id Git.Git -e --source winget
```

### Step 2: After Git Installation
Restart your system or PowerShell, then run:

```powershell
cd C:\Users\jfern\credit
venv\Scripts\python push_to_github.py
```

### Step 3: GitHub Authentication
You'll need authentication to push. Choose one:

**Option 1: SSH Key (Recommended)**
1. Generate SSH key: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
2. Add to GitHub: https://github.com/settings/keys

**Option 2: Personal Access Token**
1. Create token: https://github.com/settings/tokens
2. Scope: `repo` (all)
3. Run this after Git installation:
```bash
git remote set-url origin https://YOUR_USERNAME:YOUR_TOKEN@github.com/jferns13-cmyk/Credit-DataScience-Project.git
```

### Quick Manual Push (Alternative)
After Git is installed, run these commands:

```powershell
cd C:\Users\jfern\credit

# Initialize repo
git init

# Configure user
git config user.name "jferns13-cmyk"
git config user.email "jferns13@gmail.com"

# Add remote
git remote add origin https://github.com/jferns13-cmyk/Credit-DataScience-Project.git

# Create .gitignore (included in push_to_github.py)

# Add files
git add .
git commit -m "Initial commit: Credit classification ML project"

# Push
git branch -M main
git push -u origin main
```

### Repository Details
- **URL**: https://github.com/jferns13-cmyk/Credit-DataScience-Project
- **Username**: jferns13-cmyk
- **Email**: jferns13@gmail.com

---

**📝 Files to be pushed:**
- ml_pipeline.py
- streamlit_app.py
- push_to_github.py
- models/best_model.pkl
- models/scaler.pkl
- models/model_results.csv
- README.md (will be created)
- requirements.txt (will be created)
- .gitignore (will be created)
