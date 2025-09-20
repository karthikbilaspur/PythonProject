# Import necessary libraries
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

# Load the dataset
def load_dataset():
    # Replace with your dataset
    from sklearn.datasets import load_iris
    iris = load_iris()
    X = iris.data
    y = iris.target
    return X, y

# Define the machine learning models
def define_models():
    models = {
        'Random Forest': RandomForestClassifier(),
        'SVM': SVC(),
        'Logistic Regression': LogisticRegression(max_iter=1000),
        'Decision Tree': DecisionTreeClassifier(),
        'Naive Bayes': GaussianNB(),
        'K-Nearest Neighbors': KNeighborsClassifier(),
        'Gradient Boosting': GradientBoostingClassifier(),
        'Neural Network': MLPClassifier(max_iter=1000)
    }
    return models

# Define the hyperparameter tuning spaces
def define_param_grids():
    param_grids = {
        'Random Forest': {'n_estimators': [100, 200, 500], 'max_depth': [None, 5, 10]},
        'SVM': {'C': [0.1, 1, 10], 'kernel': ['linear', 'rbf', 'poly']},
        'Logistic Regression': {'C': [0.1, 1, 10], 'penalty': ['l1', 'l2']},
        'Decision Tree': {'max_depth': [None, 5, 10], 'min_samples_split': [2, 5, 10]},
        'Naive Bayes': {'var_smoothing': [1e-9, 1e-8, 1e-7]},
        'K-Nearest Neighbors': {'n_neighbors': [3, 5, 7], 'weights': ['uniform', 'distance']},
        'Gradient Boosting': {'n_estimators': [100, 200, 500], 'max_depth': [3, 5, 10]},
        'Neural Network': {'hidden_layer_sizes': [(50, 50), (100, 100)], 'activation': ['relu', 'tanh']}
    }
    return param_grids

# Perform grid search and evaluate models
def evaluate_models(X_train, X_test, y_train, y_test):
    models = define_models()
    param_grids = define_param_grids()
    results = {}
    
    for name, model in models.items():
        grid_search = GridSearchCV(model, param_grids[name], cv=5)
        grid_search.fit(X_train, y_train)
        y_pred = grid_search.predict(X_test)
        results[name] = {
            'Best Parameters': grid_search.best_params_,
            'Best Score': grid_search.best_score_,
            'Accuracy': accuracy_score(y_test, y_pred),
            'Classification Report': classification_report(y_test, y_pred),
            'Confusion Matrix': confusion_matrix(y_test, y_pred)
        }
    
    return results

# Main function
def main():
    X, y = load_dataset()
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    results = evaluate_models(X_train, X_test, y_train, y_test)
    
    for name, result in results.items():
        print(name)
        print("Best Parameters: ", result['Best Parameters'])
        print("Best Score: ", result['Best Score'])
        print("Accuracy: ", result['Accuracy'])
        print("Classification Report:\n", result['Classification Report'])
        print("Confusion Matrix:\n", result['Confusion Matrix'])
        print("\n")

if __name__ == "__main__":
    main()