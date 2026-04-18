"""
Credit Approval Classification ML Pipeline
Preprocesses data and trains multiple classification algorithms
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, confusion_matrix, 
                             classification_report, roc_curve, auc)
import pickle
import os

# Configuration
RANDOM_STATE = 42
TEST_SIZE = 0.2
MODEL_DIR = "models"

# Create models directory if it doesn't exist
os.makedirs(MODEL_DIR, exist_ok=True)

class CreditClassificationPipeline:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.models = {}
        self.results = {}
        self.best_model = None
        self.best_model_name = None
        
    def load_data(self):
        """Load the CSV file"""
        print("Loading data...")
        self.df = pd.read_csv(self.data_path)
        print(f"Data shape: {self.df.shape}")
        print(f"Columns: {self.df.columns.tolist()}")
        return self.df
    
    def preprocess(self):
        """Preprocess the data"""
        print("\n" + "="*50)
        print("PREPROCESSING")
        print("="*50)
        
        # Separate features and target
        X = self.df.drop('approved', axis=1)
        y = self.df['approved']
        
        print(f"\nOriginal data shape: X={X.shape}, y={y.shape}")
        print(f"Target distribution:\n{y.value_counts()}")
        print(f"Target percentages:\n{y.value_counts(normalize=True)}")
        
        # Check for missing values
        print(f"\nMissing values:\n{X.isnull().sum()}")
        
        # Handle any missing values (drop if any exist)
        X = X.dropna()
        y = y[X.index]
        
        # Feature statistics
        print(f"\nFeature statistics:")
        print(X.describe())
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
        )
        
        print(f"\nTraining set size: {self.X_train.shape}")
        print(f"Test set size: {self.X_test.shape}")
        
        # Feature scaling
        print("\nApplying Standard Scaling...")
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        print("Scaling completed!")
        
        return self.X_train_scaled, self.X_test_scaled, self.y_train, self.y_test
    
    def train_models(self):
        """Train multiple classification algorithms"""
        print("\n" + "="*50)
        print("TRAINING MODELS")
        print("="*50)
        
        # Define models
        models_to_train = {
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
            'Decision Tree': DecisionTreeClassifier(random_state=RANDOM_STATE, max_depth=10),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=RANDOM_STATE),
            'SVM': SVC(kernel='rbf', probability=True, random_state=RANDOM_STATE),
            'KNN': KNeighborsClassifier(n_neighbors=5, n_jobs=-1)
        }
        
        for name, model in models_to_train.items():
            print(f"\nTraining {name}...")
            model.fit(self.X_train_scaled, self.y_train)
            self.models[name] = model
            print(f"{name} training completed!")
    
    def evaluate_models(self):
        """Evaluate all models"""
        print("\n" + "="*50)
        print("MODEL EVALUATION")
        print("="*50)
        
        for name, model in self.models.items():
            print(f"\n{'='*40}")
            print(f"Model: {name}")
            print(f"{'='*40}")
            
            # Predictions
            y_pred = model.predict(self.X_test_scaled)
            
            # Metrics
            accuracy = accuracy_score(self.y_test, y_pred)
            precision = precision_score(self.y_test, y_pred)
            recall = recall_score(self.y_test, y_pred)
            f1 = f1_score(self.y_test, y_pred)
            
            # For models with probability prediction
            if hasattr(model, 'predict_proba'):
                y_proba = model.predict_proba(self.X_test_scaled)[:, 1]
                roc_auc = roc_auc_score(self.y_test, y_proba)
            else:
                roc_auc = None
            
            # Cross-validation score
            cv_scores = cross_val_score(model, self.X_train_scaled, self.y_train, cv=5)
            
            self.results[name] = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1': f1,
                'roc_auc': roc_auc,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'y_pred': y_pred,
                'y_proba': y_proba if hasattr(model, 'predict_proba') else None,
                'confusion_matrix': confusion_matrix(self.y_test, y_pred),
                'classification_report': classification_report(self.y_test, y_pred)
            }
            
            print(f"Accuracy:  {accuracy:.4f}")
            print(f"Precision: {precision:.4f}")
            print(f"Recall:    {recall:.4f}")
            print(f"F1 Score:  {f1:.4f}")
            if roc_auc:
                print(f"ROC AUC:   {roc_auc:.4f}")
            print(f"CV (5-fold) - Mean: {cv_scores.mean():.4f}, Std: {cv_scores.std():.4f}")
            print(f"\n{self.results[name]['classification_report']}")
    
    def find_best_model(self):
        """Find the best model based on F1 score"""
        print("\n" + "="*50)
        print("BEST MODEL SELECTION")
        print("="*50)
        
        best_f1 = -1
        for name, metrics in self.results.items():
            if metrics['f1'] > best_f1:
                best_f1 = metrics['f1']
                self.best_model_name = name
                self.best_model = self.models[name]
        
        print(f"\nBest Model: {self.best_model_name}")
        print(f"F1 Score: {self.results[self.best_model_name]['f1']:.4f}")
        print(f"Accuracy: {self.results[self.best_model_name]['accuracy']:.4f}")
        
        return self.best_model_name, self.best_model
    
    def save_model(self):
        """Save the best model and scaler"""
        print(f"\nSaving best model ({self.best_model_name})...")
        
        model_path = os.path.join(MODEL_DIR, f"best_model.pkl")
        scaler_path = os.path.join(MODEL_DIR, "scaler.pkl")
        
        with open(model_path, 'wb') as f:
            pickle.dump(self.best_model, f)
        
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        print(f"Model saved to {model_path}")
        print(f"Scaler saved to {scaler_path}")
    
    def save_results(self):
        """Save results summary"""
        results_df = pd.DataFrame({
            'Model': self.results.keys(),
            'Accuracy': [self.results[m]['accuracy'] for m in self.results.keys()],
            'Precision': [self.results[m]['precision'] for m in self.results.keys()],
            'Recall': [self.results[m]['recall'] for m in self.results.keys()],
            'F1 Score': [self.results[m]['f1'] for m in self.results.keys()],
            'ROC AUC': [self.results[m]['roc_auc'] if self.results[m]['roc_auc'] else 0 for m in self.results.keys()],
            'CV Mean': [self.results[m]['cv_mean'] for m in self.results.keys()],
        })
        
        results_df = results_df.sort_values('F1 Score', ascending=False)
        results_df.to_csv(os.path.join(MODEL_DIR, 'model_results.csv'), index=False)
        print(f"\nResults saved to {os.path.join(MODEL_DIR, 'model_results.csv')}")
        print("\nModel Comparison:")
        print(results_df.to_string(index=False))
    
    def run_pipeline(self):
        """Run the complete pipeline"""
        self.load_data()
        self.preprocess()
        self.train_models()
        self.evaluate_models()
        self.find_best_model()
        self.save_model()
        self.save_results()
        
        return self.best_model_name, self.results

if __name__ == "__main__":
    data_path = r"C:\Users\jfern\credit\credit (3) (1).csv"
    
    pipeline = CreditClassificationPipeline(data_path)
    best_model, results = pipeline.run_pipeline()
    
    print("\n" + "="*50)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*50)
