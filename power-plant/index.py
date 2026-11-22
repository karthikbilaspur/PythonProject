import joblib  # pyright: ignore[reportMissingTypeStubs]
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Any, cast
from numpy.typing import NDArray
from sklearn.ensemble import RandomForestRegressor  # pyright: ignore[reportMissingTypeStubs]
from sklearn.metrics import (  # pyright: ignore[reportMissingTypeStubs,reportUnknownVariableType]
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import (  # pyright: ignore[reportMissingTypeStubs]
    cross_val_score,
    train_test_split,
)

DATA_FILE = Path("power_plant_data.csv")
MODEL_FILE = Path("power_plant_model.pkl")
TARGET = "energy_output"

def load_or_demo() -> pd.DataFrame:
    if DATA_FILE.exists():
        df = pd.read_csv(DATA_FILE)
        print(f"Loaded {DATA_FILE} - {df.shape[0]} rows, {df.shape[1]} cols")
        return df
    print("No CSV found - generating synthetic demo data...")
    rng = np.random.default_rng(42); n = 1000
    temp = rng.uniform(10, 35, n); hum = rng.uniform(30, 90, n); wind = rng.uniform(0, 20, n); pressure = rng.uniform(990, 1030, n)
    y = 480 - 2.0*temp - 0.5*hum + 0.8*wind + 0.1*(pressure-1010) + rng.normal(0, 8, n)
    df = pd.DataFrame({"temperature": temp, "humidity": hum, "wind_speed": wind, "pressure": pressure, TARGET: y})
    df.to_csv(DATA_FILE, index=False); print(f"Demo saved to {DATA_FILE}")
    return df

def validate(df: pd.DataFrame) -> pd.DataFrame:
    if TARGET not in df.columns: raise ValueError(f"CSV must have '{TARGET}' column. Found: {list(df.columns)}")
    if df.isna().sum().sum(): print(f"Warning: {df.isna().sum().sum()} missing values - filling with median"); df = df.fillna(df.median(numeric_only=True))
    if len(df) < 50: raise ValueError("Need at least 50 rows")
    return df

def evaluate(y_true: pd.Series[Any] | NDArray[np.float64], y_pred: pd.Series[Any] | NDArray[np.float64], label: str = "") -> float:
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    print(f"{label} RMSE: {rmse:.2f} | MAE: {mae:.2f} | R2: {r2:.3f}")
    return rmse

def main():
    df = validate(load_or_demo())
    feature_cols = [c for c in df.columns if c != TARGET]
    if not feature_cols:
        raise ValueError("CSV must contain at least one feature column")

    print(f"Features: {feature_cols}")
    X = df[feature_cols]
    y = df[TARGET]
    X_train, X_test, y_train, y_test = cast(
        tuple[pd.DataFrame, pd.DataFrame, pd.Series[Any], pd.Series[Any]],
        train_test_split(X, y, test_size=0.2, random_state=42),
    )

    model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1, max_depth=12)
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring="neg_root_mean_squared_error")
    print(f"CV RMSE: {-scores.mean():.2f} (+/- {scores.std():.2f})")

    model.fit(X_train, y_train)
    predictions = cast(NDArray[np.float64], model.predict(X_test))
    evaluate(y_test, predictions, "Test")

    imp = pd.Series(model.feature_importances_, index=feature_cols).sort_values(ascending=False)
    print("\nFeature importance:")
    print(imp.to_string())

    joblib.dump({"model": model, "features": feature_cols}, MODEL_FILE)
    print(f"\nModel saved to {MODEL_FILE}")
    print("\n--- Interactive prediction (type 'quit' to exit) ---")

    while True:
        vals: dict[str, float] = {}
        for col in feature_cols:
            raw = input(f"{col} [{df[col].min():.1f}-{df[col].max():.1f}]: ").strip()
            if raw.lower() in ("quit", "q", "exit"):
                print("Goodbye!")
                return
            try:
                vals[col] = float(raw)
            except ValueError:
                print("Enter a number.")
                break
        else:
            prediction = float(cast(NDArray[np.float64], model.predict(pd.DataFrame([vals])))[0])
            print(f"Predicted {TARGET}: {prediction:.2f}\n")

if __name__ == "__main__":
    main()
