"""
Streamlit Web App for Credit Approval Classification
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Credit Approval Classifier",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .header-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 10px;
        color: white;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# Load model and scaler
@st.cache_resource
def load_model_and_scaler():
    with open('models/best_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    return model, scaler

# Load dataset for statistics
@st.cache_data
def load_dataset():
    df = pd.read_csv(r"C:\Users\jfern\credit\credit (3) (1).csv")
    return df

# Load model results
@st.cache_data
def load_results():
    results_df = pd.read_csv('models/model_results.csv')
    return results_df

try:
    model, scaler = load_model_and_scaler()
    df_original = load_dataset()
    results_df = load_results()
except FileNotFoundError:
    st.error("Model files not found. Please run ml_pipeline.py first.")
    st.stop()

# Header
st.markdown("""
    <div class="header-section">
        <h1>💳 Credit Approval Classification System</h1>
        <p>Advanced machine learning model to predict credit approval with high accuracy</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Select Page:", 
    ["🏠 Home", "🔮 Make Prediction", "📈 Model Performance", "📊 Data Analysis", "ℹ️ About"])

# ===== PAGE: HOME =====
if page == "🏠 Home":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Best Model", "Random Forest", "94% Accuracy")
    with col2:
        st.metric("F1 Score", "0.9048", "↑ Excellent")
    with col3:
        st.metric("Total Samples", len(df_original), "Trained on")
    
    st.markdown("---")
    
    st.subheader("🎯 Key Features")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("""
        ✅ **6 Classification Algorithms Tested**
        - Logistic Regression
        - Decision Tree
        - Random Forest (Best)
        - Gradient Boosting
        - Support Vector Machine
        - K-Nearest Neighbors
        """)
    
    with col2:
        st.write("""
        ✅ **Preprocessing Applied**
        - Feature scaling (StandardScaler)
        - Train-test split (80-20)
        - Stratified sampling
        - Cross-validation (5-fold)
        
        ✅ **High Performance**
        - 94% Accuracy
        - 98.3% Recall
        - 83.8% Precision
        """)
    
    st.markdown("---")
    st.subheader("📋 Dataset Overview")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(f"**Total Records:** {len(df_original)}")
        st.write(f"**Features:** 5 (Age, Income, Years at Job, Credit Score, Existing Cards)")
        st.write(f"**Target:** Approved (0=Rejected, 1=Approved)")
        
    with col2:
        approved_counts = df_original['approved'].value_counts()
        fig = go.Figure(data=[go.Pie(labels=['Rejected', 'Approved'], 
                                      values=approved_counts.values,
                                      hole=0.3)])
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)

# ===== PAGE: MAKE PREDICTION =====
elif page == "🔮 Make Prediction":
    st.subheader("🔮 Make a Credit Approval Prediction")
    st.write("Enter the applicant details below to predict credit approval.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.slider("Age", min_value=18, max_value=100, value=40, step=1)
        years_at_job = st.slider("Years at Job", min_value=0, max_value=50, value=5, step=1)
        existing_credit_cards = st.slider("Existing Credit Cards", min_value=0, max_value=10, value=2, step=1)
    
    with col2:
        income = st.number_input("Annual Income ($)", min_value=5000, max_value=150000, value=50000, step=1000)
        credit_score = st.slider("Credit Score", min_value=300, max_value=850, value=650, step=10)
    
    if st.button("🔍 Predict", use_container_width=True, type="primary"):
        # Prepare input data
        input_data = np.array([[age, income, years_at_job, credit_score, existing_credit_cards]])
        input_scaled = scaler.transform(input_data)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0]
        
        # Display results
        st.markdown("---")
        st.subheader("📊 Prediction Results")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            status = "✅ APPROVED" if prediction == 1 else "❌ REJECTED"
            st.metric("Decision", status)
        
        with col2:
            approval_prob = probability[1] * 100 if prediction == 1 else probability[0] * 100
            st.metric("Confidence", f"{approval_prob:.1f}%")
        
        with col3:
            st.metric("Probability", f"{probability[prediction]:.2%}")
        
        # Probability distribution
        st.markdown("---")
        fig = go.Figure(data=[
            go.Bar(x=['Rejected', 'Approved'], y=probability, 
                   marker_color=['#ff6b6b', '#51cf66'],
                   text=[f'{p:.1%}' for p in probability],
                   textposition='auto')
        ])
        fig.update_layout(title="Prediction Probability Distribution", 
                         yaxis_title="Probability",
                         showlegend=False,
                         height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary
        st.markdown("---")
        st.subheader("📋 Applicant Summary")
        summary_df = pd.DataFrame({
            'Feature': ['Age', 'Income', 'Years at Job', 'Credit Score', 'Existing Cards'],
            'Value': [age, f'${income:,.0f}', years_at_job, credit_score, existing_credit_cards]
        })
        st.table(summary_df)

# ===== PAGE: MODEL PERFORMANCE =====
elif page == "📈 Model Performance":
    st.subheader("📈 Model Comparison & Performance Metrics")
    
    # Model comparison table
    st.write("**All 6 Models Ranked by F1 Score:**")
    st.dataframe(results_df.style.highlight_max(subset='F1 Score', color='#51cf66').
                 highlight_min(subset='F1 Score', color='#ff6b6b'),
                 use_container_width=True)
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Accuracy comparison
        fig_accuracy = px.bar(results_df.sort_values('Accuracy', ascending=True),
                             x='Accuracy', y='Model', orientation='h',
                             color='Accuracy', color_continuous_scale='Blues',
                             title='Model Accuracy Comparison')
        fig_accuracy.update_layout(height=400)
        st.plotly_chart(fig_accuracy, use_container_width=True)
    
    with col2:
        # F1 Score comparison
        fig_f1 = px.bar(results_df.sort_values('F1 Score', ascending=True),
                       x='F1 Score', y='Model', orientation='h',
                       color='F1 Score', color_continuous_scale='Greens',
                       title='F1 Score Comparison')
        fig_f1.update_layout(height=400)
        st.plotly_chart(fig_f1, use_container_width=True)
    
    # Metrics radar chart
    col1, col2 = st.columns([1, 2])
    with col2:
        best_model_metrics = results_df[results_df['Model'] == 'Random Forest'].iloc[0]
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=[best_model_metrics['Accuracy'], best_model_metrics['Precision'], 
               best_model_metrics['Recall'], best_model_metrics['F1 Score'],
               best_model_metrics['ROC AUC'], best_model_metrics['CV Mean']],
            theta=['Accuracy', 'Precision', 'Recall', 'F1 Score', 'ROC AUC', 'CV Mean'],
            fill='toself',
            name='Random Forest'
        ))
        fig_radar.update_layout(title='Random Forest - Performance Metrics', height=400)
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col1:
        st.write("**Best Model Detailed Metrics:**")
        st.metric("Accuracy", f"{best_model_metrics['Accuracy']:.1%}")
        st.metric("Precision", f"{best_model_metrics['Precision']:.1%}")
        st.metric("Recall", f"{best_model_metrics['Recall']:.1%}")
        st.metric("F1 Score", f"{best_model_metrics['F1 Score']:.1%}")
        st.metric("ROC AUC", f"{best_model_metrics['ROC AUC']:.1%}")

# ===== PAGE: DATA ANALYSIS =====
elif page == "📊 Data Analysis":
    st.subheader("📊 Dataset Analysis & Insights")
    
    # Dataset statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Dataset Statistics:**")
        st.dataframe(df_original.describe(), use_container_width=True)
    
    with col2:
        st.write("**Target Distribution:**")
        approved_dist = df_original['approved'].value_counts()
        fig = go.Figure(data=[
            go.Bar(x=['Rejected', 'Approved'], 
                   y=approved_dist.values,
                   marker_color=['#ff6b6b', '#51cf66'],
                   text=approved_dist.values,
                   textposition='auto')
        ])
        fig.update_layout(title='Credit Approval Distribution', height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Feature distributions
    st.write("**Feature Distributions:**")
    
    features = ['age', 'income', 'years_at_job', 'credit_score', 'existing_credit_cards']
    cols = st.columns(2)
    
    for idx, feature in enumerate(features):
        with cols[idx % 2]:
            fig = px.histogram(df_original, x=feature, nbins=30, 
                              title=f'{feature.replace("_", " ").title()} Distribution',
                              color_discrete_sequence=['#667eea'])
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
    
    # Correlation with approval
    st.markdown("---")
    st.write("**Feature Correlation with Approval:**")
    
    correlations = df_original.corr()['approved'].drop('approved').sort_values(ascending=False)
    fig_corr = px.bar(x=correlations.values, y=correlations.index,
                     orientation='h', color=correlations.values,
                     color_continuous_scale='RdBu',
                     title='Feature Correlation with Credit Approval')
    fig_corr.update_layout(height=400)
    st.plotly_chart(fig_corr, use_container_width=True)

# ===== PAGE: ABOUT =====
else:  # About
    st.subheader("ℹ️ About This Application")
    
    st.write("""
    ## 📌 Project Overview
    
    This credit approval classification system uses advanced machine learning techniques to predict 
    whether a credit application should be approved or rejected based on applicant characteristics.
    
    ### 🔬 Methodology
    
    **Data Preprocessing:**
    - Feature scaling using StandardScaler for numerical stability
    - Train-test split: 80% training, 20% testing
    - Stratified sampling to maintain class distribution
    - 5-fold cross-validation for robust evaluation
    
    **Models Trained & Evaluated:**
    1. Logistic Regression (87.1% CV Mean)
    2. Decision Tree (94.1% CV Mean)
    3. Random Forest (96.0% CV Mean) ⭐ **BEST**
    4. Gradient Boosting (95.0% CV Mean)
    5. Support Vector Machine (92.0% CV Mean)
    6. K-Nearest Neighbors (88.1% CV Mean)
    
    ### 🏆 Best Model: Random Forest
    
    **Performance Metrics:**
    - Accuracy: 94.0%
    - Precision: 83.8%
    - Recall: 98.3%
    - F1 Score: 0.9048
    - ROC AUC: 0.9379
    
    **Advantages:**
    - Handles non-linear relationships well
    - Robust to outliers
    - Provides feature importance
    - Excellent generalization
    
    ### 📊 Dataset
    
    - **Total Samples:** 1,000
    - **Features:** 5 (Age, Income, Years at Job, Credit Score, Existing Cards)
    - **Target:** Approval (0=Rejected, 1=Approved)
    - **Class Distribution:** 71.1% Rejected, 28.9% Approved
    
    ### 🎯 Features Used
    
    1. **Age** - Applicant's age in years
    2. **Income** - Annual income in dollars
    3. **Years at Job** - How long at current job
    4. **Credit Score** - Credit score (300-850)
    5. **Existing Credit Cards** - Number of existing credit cards
    
    ### 📱 How to Use
    
    1. Go to **"🔮 Make Prediction"** tab
    2. Enter applicant details
    3. Click **"Predict"** button
    4. View approval probability and decision
    
    ### 🔗 Technologies Used
    
    - **Python 3.14**
    - **Streamlit** - Web framework
    - **Scikit-learn** - Machine learning
    - **Pandas** - Data manipulation
    - **Plotly** - Data visualization
    
    ### 📝 Author Notes
    
    This model is trained on historical credit approval data and demonstrates strong predictive 
    performance. However, real-world credit decisions should incorporate additional factors and 
    comply with fair lending regulations.
    """)
    
    st.markdown("---")
    st.info("💡 Tip: Use the 'Make Prediction' tab to test the model with different applicant profiles!")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px; padding: 20px;'>
        <p>Credit Approval Classification System | Powered by Machine Learning | 2026</p>
    </div>
    """, unsafe_allow_html=True)
