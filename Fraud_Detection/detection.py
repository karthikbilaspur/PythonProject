import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

# Load the datasets
transaction_df = pd.read_csv('train_transaction.csv')
identity_df = pd.read_csv('train_identity.csv')

# Merge the datasets
df = pd.merge(transaction_df, identity_df, on='TransactionID', how='left')

# Handle missing values
def handle_missing_values(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('Unknown')
        else:
            df[col] = df[col].fillna(-999)
    return df

df = handle_missing_values(df)

# Encode categorical features
def encode_categorical_features(df):
    categorical_cols = df.select_dtypes(include=['object']).columns
    le = LabelEncoder()
    for col in categorical_cols:
        df[col] = le.fit_transform(df[col])
    return df

df = encode_categorical_features(df)

# Split the data
X = df.drop(['isFraud', 'TransactionID'], axis=1)
y = df['isFraud']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a LightGBM model
model = lgb.LGBMClassifier(objective='binary', metric='auc', boosting_type='gbdt', num_leaves=31, learning_rate=0.05)
model.fit(X_train, y_train, eval_set=[(X_test, y_test)], early_stopping_rounds=5)

# Evaluate the model
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, y_pred_proba)
accuracy = accuracy_score(y_test, y_pred)
print(f'AUC-ROC: {auc:.4f}')
print(f'Accuracy: {accuracy:.4f}')
print('Classification Report:')
print(classification_report(y_test, y_pred))
print('Confusion Matrix:')
print(confusion_matrix(y_test, y_pred))

# Feature importance
feature_importance = model.feature_importances_
feature_importance_df = pd.DataFrame({'feature': X.columns, 'importance': feature_importance})
feature_importance_df = feature_importance_df.sort_values(by='importance', ascending=False)
print(feature_importance_df.head(10))

# Plot the feature importance
plt.figure(figsize=(10, 6))
sns.barplot(x='feature', y='importance', data=feature_importance_df.head(10))
plt.title('Feature Importance')
plt.xlabel('Feature')
plt.ylabel('Importance')
plt.show()