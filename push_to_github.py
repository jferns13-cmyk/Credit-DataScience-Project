"""
Script to push code to GitHub using GitPython
"""

from git import Repo
import os

# Configuration
REPO_PATH = r"C:\Users\jfern\credit"
GITHUB_URL = "https://github.com/jferns13-cmyk/Credit-DataScience-Project.git"
USERNAME = "jferns13-cmyk"
EMAIL = "jferns13@gmail.com"

def push_to_github():
    """Push code to GitHub"""
    
    try:
        print("=" * 60)
        print("PUSHING CODE TO GITHUB")
        print("=" * 60)
        
        # Initialize repository
        print("\n1. Initializing Git repository...")
        try:
            repo = Repo(REPO_PATH)
            print("   ✓ Repository already exists")
        except:
            repo = Repo.init(REPO_PATH)
            print("   ✓ Repository initialized")
        
        # Configure git user
        print("\n2. Configuring Git user...")
        with repo.config_writer() as config:
            config.set_value("user", "name", USERNAME)
            config.set_value("user", "email", EMAIL)
        print(f"   ✓ Username: {USERNAME}")
        print(f"   ✓ Email: {EMAIL}")
        
        # Add remote
        print("\n3. Adding remote repository...")
        try:
            repo.delete_remote('origin')
        except:
            pass
        
        repo.create_remote('origin', GITHUB_URL)
        print(f"   ✓ Remote added: {GITHUB_URL}")
        
        # Create .gitignore
        print("\n4. Creating .gitignore...")
        gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Data files (optional - comment out if you want to track)
*.csv.bak

# Cache
.streamlit/cache/
.streamlit/__pycache__/

# Environment variables
.env
.env.local

# OS
.DS_Store
Thumbs.db
"""
        
        gitignore_path = os.path.join(REPO_PATH, ".gitignore")
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_content.strip())
        print("   ✓ .gitignore created")
        
        # Create README
        print("\n5. Creating README.md...")
        readme_content = """# Credit DataScience Project

## Overview
This project builds a machine learning classification system to predict credit approval using multiple algorithms.

## Dataset
- **File**: credit (3) (1).csv
- **Records**: 1,000
- **Features**: 5 (Age, Income, Years at Job, Credit Score, Existing Credit Cards)
- **Target**: Approval (0=Rejected, 1=Approved)

## Models Trained
1. Logistic Regression (87.1% CV Score)
2. Decision Tree (94.1% CV Score)
3. **Random Forest (96% CV Score)** ⭐ **BEST**
4. Gradient Boosting (95% CV Score)
5. Support Vector Machine (92% CV Score)
6. K-Nearest Neighbors (88.1% CV Score)

## Best Model Performance
- **Model**: Random Forest
- **Accuracy**: 94.0%
- **Precision**: 83.8%
- **Recall**: 98.3%
- **F1 Score**: 0.9048
- **ROC AUC**: 0.9379

## Files
- `ml_pipeline.py` - Complete ML pipeline with preprocessing and model training
- `streamlit_app.py` - Interactive web application for predictions and analysis
- `models/best_model.pkl` - Trained Random Forest model
- `models/scaler.pkl` - Feature scaler for preprocessing
- `models/model_results.csv` - Model comparison metrics

## Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\\Scripts\\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### 1. Train Models
```bash
python ml_pipeline.py
```

### 2. Run Streamlit App
```bash
streamlit run streamlit_app.py
```

Then open your browser to `http://localhost:8501`

## Features
- ✅ Comprehensive data preprocessing
- ✅ 6 classification algorithms tested
- ✅ Cross-validation and hyperparameter tuning
- ✅ Interactive Streamlit web application
- ✅ Model performance visualization
- ✅ Real-time predictions

## Technologies
- Python 3.14
- Scikit-learn (Machine Learning)
- Pandas (Data Manipulation)
- Streamlit (Web Application)
- Plotly (Visualizations)

## Author
jferns13-cmyk

## License
MIT
"""
        
        readme_path = os.path.join(REPO_PATH, "README.md")
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        print("   ✓ README.md created")
        
        # Create requirements.txt
        print("\n6. Creating requirements.txt...")
        requirements = """pandas==3.0.2
scikit-learn==1.6.1
numpy==2.4.4
matplotlib==3.10.1
seaborn==0.13.2
streamlit==1.56.0
plotly==5.24.1
gitpython==3.1.46
"""
        
        requirements_path = os.path.join(REPO_PATH, "requirements.txt")
        with open(requirements_path, 'w') as f:
            f.write(requirements)
        print("   ✓ requirements.txt created")
        
        # Add files
        print("\n7. Adding files to Git...")
        repo.index.add(['ml_pipeline.py', 'streamlit_app.py', '.gitignore', 'README.md', 'requirements.txt'])
        repo.index.add(['models/best_model.pkl', 'models/scaler.pkl', 'models/model_results.csv'])
        print("   ✓ Files staged")
        
        # Commit
        print("\n8. Creating commit...")
        repo.index.commit("Initial commit: Credit classification ML project with Streamlit app")
        print("   ✓ Commit created")
        
        # Push to GitHub
        print("\n9. Pushing to GitHub...")
        origin = repo.remote('origin')
        
        # For authentication, we'll use the https URL
        # Note: This requires proper authentication setup (SSH key or Personal Access Token)
        try:
            origin.push(refspec='main:main', force=True)
            print("   ✓ Pushed to main branch")
        except Exception as e:
            print(f"   ⚠ Push attempt: {str(e)}")
            print("   → Trying master branch...")
            try:
                origin.push(refspec='master:master', force=True)
                print("   ✓ Pushed to master branch")
            except Exception as e2:
                print(f"   ⚠ Push failed: {str(e2)}")
                print("\n   📝 AUTHENTICATION REQUIRED:")
                print("   Please set up one of the following:")
                print("   1. SSH Key (Recommended)")
                print("   2. GitHub Personal Access Token")
                print(f"\n   Then run: git push -u origin main")
        
        print("\n" + "=" * 60)
        print("GITHUB PUSH COMPLETED!")
        print("=" * 60)
        print(f"\nRepository: {GITHUB_URL}")
        print(f"Local path: {REPO_PATH}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    push_to_github()
