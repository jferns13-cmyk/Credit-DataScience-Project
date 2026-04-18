# 💳 Credit Approval Classification - Machine Learning Project

## 📊 Project Overview

This project implements an advanced machine learning classification system to predict credit approval using multiple algorithms and a user-friendly Streamlit web interface.

**Best Model**: Random Forest with **94% Accuracy** and **0.9048 F1 Score**

---

## 📈 Model Performance

| Model | Accuracy | Precision | Recall | F1 Score | ROC AUC | CV Mean |
|-------|----------|-----------|--------|----------|---------|---------|
| **Random Forest** ⭐ | 94.0% | 83.8% | **98.3%** | **0.9048** | 0.9379 | 96.0% |
| Gradient Boosting | 92.5% | 83.1% | 93.1% | 0.8780 | 0.9323 | 95.0% |
| Decision Tree | 92.5% | 84.1% | 91.4% | 0.8760 | 0.9276 | 94.1% |
| SVM | 91.0% | 82.3% | 87.9% | 0.8500 | 0.9307 | 92.0% |
| KNN | 87.5% | 74.6% | 86.2% | 0.8000 | 0.9321 | 88.1% |
| Logistic Regression | 84.0% | 74.1% | 69.0% | 0.7143 | 0.9052 | 87.1% |

---

## 📋 Dataset

- **Source**: credit (3) (1).csv
- **Total Records**: 1,000
- **Features**: 5
  - Age
  - Income (Annual)
  - Years at Job
  - Credit Score
  - Existing Credit Cards
- **Target**: Approved (0 = Rejected, 1 = Approved)
- **Class Distribution**: 71.1% Rejected, 28.9% Approved
- **Missing Values**: None

---

## 🔬 Modeling Approach

### Data Preprocessing
✅ Feature Scaling (StandardScaler)
✅ Train-Test Split (80-20 stratified)
✅ Cross-Validation (5-fold)
✅ No missing values handling needed

### Algorithms Trained
1. **Logistic Regression** - Baseline model
2. **Decision Tree** - Interpretable model
3. **Random Forest** ⭐ - Ensemble method (BEST)
4. **Gradient Boosting** - Sequential ensemble
5. **SVM** - Support Vector Machine
6. **KNN** - K-Nearest Neighbors

### Evaluation Metrics
- Accuracy
- Precision
- Recall
- F1 Score
- ROC AUC
- Confusion Matrix
- Classification Report

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone repository
git clone https://github.com/jferns13-cmyk/Credit-DataScience-Project.git
cd Credit-DataScience-Project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### 1. Train Models
```bash
python ml_pipeline.py
```

This will:
- Load and preprocess the data
- Train 6 different classification algorithms
- Evaluate and compare all models
- Save the best model (Random Forest)
- Generate performance report

#### 2. Run Streamlit Web App
```bash
streamlit run streamlit_app.py
```

Then open your browser to: **http://localhost:8501**

---

## 🎯 Features

### 🏠 Home Page
- Dashboard with key metrics
- Model overview
- Dataset statistics

### 🔮 Make Prediction
- Interactive input form
- Real-time predictions
- Confidence scores
- Probability visualization

### 📈 Model Performance
- Model comparison charts
- Accuracy benchmarks
- F1 score analysis
- Performance radar chart

### 📊 Data Analysis
- Feature distributions
- Target distribution
- Correlation analysis
- Statistical insights

### ℹ️ About
- Detailed methodology
- Technology stack
- Implementation notes

---

## 📁 Project Structure

```
Credit-DataScience-Project/
├── ml_pipeline.py              # ML pipeline and model training
├── streamlit_app.py            # Streamlit web application
├── push_to_github.py           # GitHub push script
├── push_to_github.bat          # Windows batch script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── GITHUB_SETUP.md            # Setup instructions
├── credit (3) (1).csv         # Dataset
└── models/                     # Trained models
    ├── best_model.pkl         # Random Forest model
    ├── scaler.pkl             # Feature scaler
    └── model_results.csv      # Model comparison results
```

---

## 🛠️ Technologies Used

- **Python 3.14** - Programming language
- **Scikit-learn 1.6.1** - Machine learning library
- **Pandas 3.0.2** - Data manipulation
- **NumPy 2.4.4** - Numerical computing
- **Streamlit 1.56.0** - Web framework
- **Plotly 5.24.1** - Interactive visualizations
- **Matplotlib 3.10.1** - Static visualizations
- **Seaborn 0.13.2** - Statistical visualizations

---

## 📊 Key Insights

### Feature Importance (Random Forest)
The model identifies these as most important for approval decision:
1. Credit Score
2. Income
3. Years at Job
4. Existing Credit Cards
5. Age

### Model Strengths
✅ High accuracy (94%)
✅ Excellent recall (98.3%) - catches most approvable cases
✅ Good precision (83.8%) - minimizes false approvals
✅ Robust to new data (96% CV score)
✅ Fast predictions

### Use Cases
- Automated credit pre-screening
- Real-time approval decisions
- Risk assessment
- Policy evaluation

---

## 🔐 Security & Ethics

⚠️ **Important**: This model should be used as a decision support tool, not for final decisions. Real-world credit decisions should:
- Include additional factors
- Comply with fair lending regulations
- Be reviewed by human experts
- Consider protected attributes appropriately

---

## 📞 Contact

**Project Author**: jferns13-cmyk
**Email**: jferns13@gmail.com
**GitHub**: https://github.com/jferns13-cmyk

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📚 References

- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Machine Learning Best Practices](https://ml-cheatsheet.readthedocs.io/)

---

**Last Updated**: April 18, 2026
**Status**: ✅ Complete and Production Ready
