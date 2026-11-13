
"""
Combined app: heart disease training + prediction API + exercise/food logger
Usage:
    python index.py train          # train model from heart_disease_dataset.csv
    python index.py serve          # start Flask API on http://127.0.0.1:5000
    python index.py log --table exercise --date 2022-01-01 --data "Ran 5 miles"
    python index.py delete-table --table exercise
"""
import argparse
import sqlite3
from typing import Any, cast

# ---------------------------------------------------------------------------
# 1. DATABASE (exercise / food logger)
# ---------------------------------------------------------------------------

SCHEMA = {
    'exercise': """
        CREATE TABLE IF NOT EXISTS exercise (
            id INTEGER PRIMARY KEY,
            date TEXT,
            data TEXT
        );
    """,
    'food': """
        CREATE TABLE IF NOT EXISTS food (
            id INTEGER PRIMARY KEY,
            date TEXT,
            data TEXT
        );
    """
}

INSERT_QUERIES = {
    'exercise': "INSERT INTO exercise (date, data) VALUES (?, ?);",
    'food': "INSERT INTO food (date, data) VALUES (?, ?);",
}

def _validate_table(table_name: str) -> str:
    if table_name not in SCHEMA:
        raise ValueError(f"Invalid table: {table_name!r}. Must be one of {list(SCHEMA)}")
    return table_name

class Database:
    def __init__(self, db_file: str = 'data.db'):
        self.conn = sqlite3.connect(db_file)

    def __enter__(self):
        return self

    def __exit__(self, *_args: object) -> None:
        self.close()

    def close(self):
        self.conn.close()

    def create_table(self, table_name: str):
        _validate_table(table_name)
        with self.conn:
            self.conn.execute(SCHEMA[table_name])

    def create_all_tables(self):
        for t in SCHEMA:
            self.create_table(t)

    def add_data(self, table_name: str, date: str, data: str):
        _validate_table(table_name)
        query = INSERT_QUERIES[table_name]
        with self.conn:
            self.conn.execute(query, (date, data))

    def get_all(self, table_name: str):
        _validate_table(table_name)
        cur = self.conn.execute(f"SELECT id, date, data FROM {table_name} ORDER BY date;")
        return cur.fetchall()

    def delete_table(self, table_name: str):
        # SAFE: table_name is allow-listed above, never raw user input in SQL
        _validate_table(table_name)
        with self.conn:
            self.conn.execute(f"DROP TABLE IF EXISTS {table_name};")

# ---------------------------------------------------------------------------
# 2. TRAINING
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
                   'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

def train_model(csv_path: str = 'heart_disease_dataset.csv',
                model_path: str = 'heart_disease_model.pkl',
                scaler_path: str = 'scaler.pkl'):
    import pandas as pd
    from sklearn.model_selection import train_test_split, GridSearchCV  # type: ignore[reportUnknownVariableType]
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix  # type: ignore[reportUnknownVariableType]
    from sklearn.preprocessing import StandardScaler
    import joblib  # type: ignore[reportMissingTypeStubs]

    df = pd.read_csv(csv_path)
    X = df.drop('target', axis=1)
    y = df['target']

    X_train, X_test, y_train, y_test = cast(
        tuple[pd.DataFrame, pd.DataFrame, pd.Series[Any], pd.Series[Any]],
        train_test_split(X, y, test_size=0.2, random_state=42, stratify=y),
    )

    # Note: RandomForest doesn't need scaling, but we keep the scaler so the
    # API matches training exactly, and so you can swap in another model later.
    scaler = StandardScaler()
    X_train_scaled = cast(Any, scaler.fit_transform(X_train))  # type: ignore[reportUnknownMemberType]
    X_test_scaled = cast(Any, scaler.transform(X_test))  # type: ignore[reportUnknownMemberType]

    param_grid: dict[str, list[int | None]] = {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 5, 10]
    }
    grid_search = GridSearchCV(
        RandomForestClassifier(random_state=42), param_grid, cv=5
    )
    grid_search.fit(X_train_scaled, y_train)

    best_model = grid_search.best_estimator_
    best_params = cast(dict[str, int | None], grid_search.best_params_)
    print("Best params:", best_params)

    y_pred = cast(Any, best_model.predict(X_test_scaled))  # type: ignore[reportUnknownMemberType]
    print("Accuracy:", cast(Any, accuracy_score(y_test, y_pred)))
    print("Classification Report:")
    print(cast(Any, classification_report(y_test, y_pred)))
    print("Confusion Matrix:")
    print(cast(Any, confusion_matrix(y_test, y_pred)))

    cast(Any, joblib).dump(best_model, model_path)
    cast(Any, joblib).dump(scaler, scaler_path)
    print(f"Saved model -> {model_path}, scaler -> {scaler_path}")
    return best_model, scaler

# ---------------------------------------------------------------------------
# 3. FLASK API
# ---------------------------------------------------------------------------

def create_app(db_file: str = 'data.db',
               model_path: str = 'heart_disease_model.pkl',
               scaler_path: str = 'scaler.pkl'):
    from flask import Flask, request, jsonify
    import joblib  # type: ignore[reportMissingTypeStubs]
    import pandas as pd

    app = Flask(__name__)

    # Load once at startup
    try:
        model: Any = joblib.load(model_path)
        scaler: Any = joblib.load(scaler_path)
    except FileNotFoundError as e:
        raise SystemExit(
            f"Model files not found: {e}. Run 'python app.py train' first."
        )

    def validate_data(data: Any):
        if not isinstance(data, dict):
            return False, "Request body must be a JSON object"
        for field in REQUIRED_FIELDS:
            if field not in data:
                return False, f"Missing field: {field}"
            try:
                float(data[field])
            except (TypeError, ValueError):
                return False, f"Field {field} must be a number"
        return True, None

    @app.route('/predict', methods=['POST'])
    def predict():
        try:
            data = request.get_json(force=True)
            ok, err = validate_data(data)
            if not ok:
                return jsonify({'error': err}), 400

            # FIX: enforce column order from training
            features = pd.DataFrame([{f: float(data[f]) for f in REQUIRED_FIELDS}])
            features_scaled = scaler.transform(features)
            prediction = model.predict(features_scaled)
            return jsonify({'prediction': int(prediction[0])})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/log', methods=['POST'])
    def log():
        """Log exercise/food: {"table": "exercise", "date": "2022-01-01", "data": "Ran 5 miles"}"""
        try:
            data = request.get_json(force=True)
            table = data.get('table')
            date = data.get('date')
            text = data.get('data')
            if not table or not date or not text:
                return jsonify({'error': 'table, date and data are required'}), 400
            _validate_table(table)
            with Database(db_file) as db:
                db.create_table(table)
                db.add_data(table, date, text)
            return jsonify({'status': 'ok'})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/logs/<table>', methods=['GET'])
    def get_logs(table: str):
        try:
            _validate_table(table)
            with Database(db_file) as db:
                db.create_table(table)
                rows = db.get_all(table)
            return jsonify([{'id': r[0], 'date': r[1], 'data': r[2]} for r in rows])
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok'})

    return app

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Heart disease app - train / serve / log")
    sub = parser.add_subparsers(dest='command', required=True)

    p_train = sub.add_parser('train', help='Train model')
    p_train.add_argument('--csv', default='heart_disease_dataset.csv')
    p_train.add_argument('--model', default='heart_disease_model.pkl')
    p_train.add_argument('--scaler', default='scaler.pkl')

    p_serve = sub.add_parser('serve', help='Start Flask API')
    p_serve.add_argument('--host', default='127.0.0.1')
    p_serve.add_argument('--port', type=int, default=5000)
    p_serve.add_argument('--db', default='data.db')
    p_serve.add_argument('--debug', action='store_true', help='Dev only, never in production')

    p_log = sub.add_parser('log', help='Log exercise/food to SQLite')
    p_log.add_argument('--table', required=True, choices=list(SCHEMA))
    p_log.add_argument('--date', required=True)
    p_log.add_argument('--data', required=True)
    p_log.add_argument('--db', default='data.db')

    p_del = sub.add_parser('delete-table', help='Delete a log table')
    p_del.add_argument('--table', required=True, choices=list(SCHEMA))
    p_del.add_argument('--db', default='data.db')

    args = parser.parse_args()

    if args.command == 'train':
        train_model(args.csv, args.model, args.scaler)

    elif args.command == 'serve':
        app = create_app(db_file=args.db)
        # debug=False by default - only enable with --debug locally
        app.run(host=args.host, port=args.port, debug=args.debug)

    elif args.command == 'log':
        with Database(args.db) as db:
            db.create_table(args.table)
            db.add_data(args.table, args.date, args.data)
        print(f"Logged to {args.table}: {args.date} - {args.data}")

    elif args.command == 'delete-table':
        with Database(args.db) as db:
            db.delete_table(args.table)
        print(f"Deleted table {args.table}")

if __name__ == '__main__':
    main()
