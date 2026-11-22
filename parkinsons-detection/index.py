from __future__ import annotations

import sys
from typing import Any, cast

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (  # pyright: ignore[reportUnknownVariableType]
    accuracy_score,  # pyright: ignore[reportUnknownVariableType]
    balanced_accuracy_score,  # pyright: ignore[reportUnknownVariableType]
    classification_report,  # pyright: ignore[reportUnknownVariableType]
    confusion_matrix,  # pyright: ignore[reportUnknownVariableType]
)
from sklearn.model_selection import (  # pyright: ignore[reportUnknownVariableType]
    StratifiedKFold,  # pyright: ignore[reportUnknownVariableType]
    cross_val_score,  # pyright: ignore[reportUnknownVariableType]
    train_test_split,  # pyright: ignore[reportUnknownVariableType]
)

CSV_PATH = "spiral_drawings.csv"
TARGET_COL = "label"
TEST_SIZE = 0.2
RANDOM_STATE = 42


# -------------------- Data loading / validation --------------------
def load_data(path: str = CSV_PATH) -> tuple[pd.DataFrame, pd.Series]:
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"File not found: '{path}'. Check the file path / working directory."
        ) from None

    if df.empty:
        raise ValueError("Dataset is empty.")

    if TARGET_COL not in df.columns:
        raise ValueError(
            f"'{TARGET_COL}' column not found. Found columns: {list(df.columns)}"
        )

    features_df = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL]

    if features_df.empty or features_df.shape[1] == 0:
        raise ValueError("No feature columns left after dropping 'label'.")

    # --- Non-numeric columns: RF can't handle strings ---
    non_numeric = features_df.select_dtypes(exclude=[np.number]).columns.tolist()
    if non_numeric:
        raise ValueError(
            f"Non-numeric feature columns found: {non_numeric}. "
            "Encode them (e.g. OneHotEncoder) or drop them before training."
        )

    # --- NaNs: RF in sklearn < 1.4 cannot handle NaN at all ---
    nan_counts = features_df.isna().sum()
    nan_counts = nan_counts[nan_counts > 0]
    if not nan_counts.empty:
        print("WARNING: NaN values found, filling with column median:")
        print(nan_counts.to_string())
        features_df = features_df.fillna(features_df.median(numeric_only=True))

    # --- Target: report class balance (critical for medical data) ---
    print("Class distribution:")
    print(y.value_counts().to_string())
    print(f"Class proportions:\n{y.value_counts(normalize=True).round(3).to_string()}\n")

    # Stratified split needs >= 2 samples per class
    min_class = y.value_counts().min()
    if min_class < 2:
        raise ValueError(
            f"Smallest class has only {min_class} sample(s). "
            "Stratified split / CV needs at least 2 per class."
        )

    return features_df, y


# -------------------- Training / evaluation --------------------
def train_and_evaluate(
    X: pd.DataFrame, y: pd.Series
) -> tuple[RandomForestClassifier, list[str], pd.DataFrame]:
    # FIX: stratify=y keeps the healthy/PD ratio same in train & test.
    split = cast(
        tuple[pd.DataFrame, pd.DataFrame, pd.Series[Any], pd.Series[Any]],
        cast(Any, train_test_split)(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
        ),
    )
    X_train, X_test, y_train, y_test = split

    clf: Any = RandomForestClassifier(
        n_estimators=300,  # 100 is fine, 300 is more stable for small data
        random_state=RANDOM_STATE,
        class_weight="balanced_subsample",  # FIX: handle imbalance
        n_jobs=-1,
    )
    clf.fit(X_train, y_train)

    # --- Cross-validation: more trustworthy than a single split ---
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cast(
        np.ndarray[Any, Any],
        cast(Any, cross_val_score)(clf, X, y, cv=cv, scoring="accuracy", n_jobs=-1),
    )
    print(f"CV accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
    print(f"CV scores per fold: {np.round(cv_scores, 3)}\n")

    # --- Held-out test set ---
    y_pred = cast(np.ndarray[Any, Any], clf.predict(X_test))
    print(f"Test accuracy:          {cast(Any, accuracy_score)(y_test, y_pred):.3f}")
    print(f"Test balanced accuracy: {cast(Any, balanced_accuracy_score)(y_test, y_pred):.3f}")
    print("\nClassification report:")
    report = cast(str, cast(Any, classification_report)(y_test, y_pred, zero_division=0))
    print(report)
    print("Confusion matrix (rows = true, cols = predicted):")
    matrix = cast(np.ndarray[Any, Any], cast(Any, confusion_matrix)(y_test, y_pred))
    print(matrix)

    # Feature importances - useful for spiral data (which features matter?)
    feature_importances = cast(np.ndarray[Any, Any], clf.feature_importances_)
    importances = pd.Series(feature_importances, index=X.columns).sort_values(ascending=False)
    print("\nTop 10 feature importances:")
    print(importances.head(10).round(4).to_string())

    return clf, list(X.columns), X_test


# -------------------- Prediction on new data --------------------
def predict_parkinsons(
    model: RandomForestClassifier,
    feature_columns: list[str],
    features: pd.DataFrame,
) -> pd.Series:
    """
    Predict on new data. Validates + REORDERS columns to training order.

    Raises ValueError on missing/extra columns instead of silently
    returning None or misaligning features.
    """
    missing = set(feature_columns) - set(features.columns)
    extra = set(features.columns) - set(feature_columns)
    if missing:
        raise ValueError(f"Missing feature columns: {sorted(missing)}")
    if extra:
        raise ValueError(f"Unexpected extra columns: {sorted(extra)}")

    # FIX: reorder to training order - sklearn uses POSITION, not names.
    aligned = features[feature_columns]

    if aligned.isna().any().any():
        raise ValueError("New data contains NaN values. Fill them before predicting.")

    preds = cast(np.ndarray[Any, Any], cast(Any, model).predict(aligned))
    return pd.Series(preds, index=features.index, name=TARGET_COL)


def main() -> int:
    try:
        X, y = load_data()
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    clf, feature_columns, X_test = train_and_evaluate(X, y)

    # --- Example usage: use REAL columns, from the test set ---
    # In real use, replace this with your own new spiral measurements,
    # with exactly the same column names as X.
    print("\n--- Example prediction on first 3 test rows (real columns) ---")
    try:
        example = X_test.iloc[:3].copy()
        preds = predict_parkinsons(clf, feature_columns, example)
        print(f"Predictions: {preds.tolist()}")
        print(f"True labels: {y.loc[example.index].tolist()}")
    except (ValueError, TypeError) as e:
        print(f"Prediction error: {e}")


    return 0


if __name__ == "__main__":
    raise SystemExit(main())