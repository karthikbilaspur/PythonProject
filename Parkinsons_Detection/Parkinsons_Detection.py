import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset
try:
    df = pd.read_csv('spiral_drawings.csv')
except FileNotFoundError:
    print("The file was not found. Please check the file path.")
    exit()

# Check if 'label' column exists
if 'label' not in df.columns:
    print("The 'label' column does not exist in the dataset.")
    exit()

# Define the features (X) and target variable (y)
X = df.drop(['label'], axis=1)
y = df['label']

# Check if X is not empty
if X.empty:
    print("The feature dataset is empty.")
    exit()

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a random forest classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Make predictions on the test set
y_pred = clf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.3f}")
print(classification_report(y_test, y_pred))

# Use the model to make predictions on new data
def predict_parkinsons(features: pd.DataFrame) -> pd.Series:
    try:
        prediction = clf.predict(features)
        return prediction
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
new_data = pd.DataFrame({
    'feature1': [1, 2, 3],
    'feature2': [4, 5, 6],
    # Add more features as needed
})

# Check if new_data has the same features as X
if set(new_data.columns) != set(X.columns):
    print("The new data does not have the same features as the training data.")
else:
    new_prediction = predict_parkinsons(new_data)
    print(f"Prediction: {new_prediction}")