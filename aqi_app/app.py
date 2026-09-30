import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import plotly.express as px

st.set_page_config(page_title="AQI Predictor", page_icon="🌫️", layout="wide")

st.title("🌫️ AQI Predictor - City Data")
st.markdown("Upload your `city_dat.csv` (10 columns, ~250 rows) and predict Air Quality Index")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    target_col = st.text_input("Target Column Name (AQI column)", value="AQI")
    test_size = st.slider("Test Size", 0.1, 0.4, 0.2)
    n_estimators = st.slider("Random Forest Trees", 50, 300, 100)

# File uploader
uploaded_file = st.file_uploader("Upload city_dat.csv", type=["csv"])

# Sample data if no file
if uploaded_file is None:
    st.info("👆 Upload your file to start. Showing demo with sample data structure.")
    # Create sample structure
    sample_data = {
        'City': ['Delhi']*25 + ['Mumbai']*25 + ['Bangalore']*25 + ['Chennai']*25,
        'PM2.5': np.random.randint(20, 300, 100),
        'PM10': np.random.randint(40, 400, 100),
        'NO': np.random.randint(1, 50, 100),
        'NO2': np.random.randint(10, 100, 100),
        'NOx': np.random.randint(10, 120, 100),
        'NH3': np.random.randint(5, 50, 100),
        'CO': np.random.uniform(0.1, 5.0, 100),
        'SO2': np.random.randint(2, 30, 100),
        'O3': np.random.randint(10, 80, 100),
        'AQI': np.random.randint(50, 350, 100)
    }
    df = pd.DataFrame(sample_data)
else:
    df = pd.read_csv(uploaded_file)

st.subheader("📊 Data Preview")
col1, col2, col3 = st.columns(3)
col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Missing Values", df.isnull().sum().sum())

st.dataframe(df.head(10), use_container_width=True)

st.subheader("📈 Data Stats")
st.write(df.describe())

# Handle preprocessing
# Auto-detect numeric and categorical
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if target_col in numeric_cols:
    numeric_cols.remove(target_col)

categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

st.write(f"**Numeric features:** {numeric_cols}")
st.write(f"**Categorical features:** {categorical_cols}")

# Encode categoricals
df_processed = df.copy()
for col in categorical_cols:
    le = LabelEncoder()
    df_processed[col] = le.fit_transform(df_processed[col].astype(str))

# Check if target exists
if target_col not in df_processed.columns:
    st.error(f"Target column '{target_col}' not found! Available: {list(df.columns)}")
    st.stop()

X = df_processed.drop(columns=[target_col])
y = df_processed[target_col]

# Drop any remaining NaN
X = X.fillna(X.median())
y = y.fillna(y.median())

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# Metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

st.subheader("✅ Model Performance")
c1, c2 = st.columns(2)
c1.metric("R² Score", f"{r2:.3f}")
c2.metric("RMSE", f"{np.sqrt(mse):.2f}")

# Feature importance
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

fig = px.bar(importance, x='importance', y='feature', orientation='h', title="Feature Importance")
st.plotly_chart(fig, use_container_width=True)

# Actual vs Predicted
fig2 = px.scatter(x=y_test, y=y_pred, labels={'x':'Actual AQI', 'y':'Predicted AQI'}, title="Actual vs Predicted AQI")
fig2.add_shape(type="line", x0=y_test.min(), y0=y_test.min(), x1=y_test.max(), y1=y_test.max(), line=dict(dash="dash"))
st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.subheader("🔮 Predict AQI for New Entry")

# Dynamic input form based on X columns
input_data = {}
cols = st.columns(3)
for i, col_name in enumerate(X.columns):
    with cols[i % 3]:
        # Use median as default
        default_val = float(X[col_name].median())
        # If original was categorical city, show text
        if col_name in [c for c in df.columns if df[c].dtype == 'object']:
            # show original labels
            options = df[col_name].unique().tolist() if col_name in df.columns else None
            # but we encoded, so we need to map back for input - keep numeric input for simplicity
            input_data[col_name] = st.number_input(f"{col_name}", value=default_val)
        else:
            input_data[col_name] = st.number_input(f"{col_name}", value=default_val)

if st.button("Predict AQI", type="primary"):
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)[0]
    
    # AQI Category
    def aqi_category(aqi):
        if aqi <= 50: return "Good 😊", "green"
        elif aqi <= 100: return "Satisfactory 🙂", "lightgreen"
        elif aqi <= 200: return "Moderate 😐", "yellow"
        elif aqi <= 300: return "Poor 😷", "orange"
        elif aqi <= 400: return "Very Poor 🤢", "red"
        else: return "Severe ☠️", "darkred"
    
    cat, color = aqi_category(prediction)
    
    st.markdown(f"""
    <div style="padding:20px;border-radius:15px;background-color:{color};color:white;text-align:center">
        <h2>Predicted AQI: {prediction:.0f}</h2>
        <h3>{cat}</h3>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("Tip: Make sure your city_dat.csv has pollutant columns like PM2.5, PM10, NO2, CO, SO2, O3 + City + AQI. 10 columns is perfect.")
