import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

# Load the dataset
df = pd.read_csv('power_plant_data.csv')

# Preprocess the data
X = df.drop(['energy_output'], axis=1)
y = df['energy_output']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a random forest regressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print(f'RMSE: {rmse:.2f}')

# Use the model to make predictions on new data
new_data = pd.DataFrame({'temperature': [25], 'humidity': [60], 'wind_speed': [10]})
new_prediction = model.predict(new_data)
print(f'Predicted energy output: {new_prediction[0]:.2f}')