import sqlite3

# Define the schema
schema = {
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

# Define the queries
queries = {
    'insert_exercise': "INSERT INTO exercise (date, data) VALUES (?, ?);",
    'insert_food': "INSERT INTO food (date, data) VALUES (?, ?);",
    'delete_table': "DROP TABLE IF EXISTS {};"
}

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)

    def create_table(self, table_name):
        with self.conn:
            self.conn.execute(schema[table_name])

    def add_data(self, table_name, date, data):
        query = queries[f'insert_{table_name}']
        with self.conn:
            self.conn.execute(query, (date, data))

    def delete_table(self, table_name):
        query = queries['delete_table'].format(table_name)
        with self.conn:
            self.conn.execute(query)

# Usage
db = Database('data.db')
db.create_table('exercise')
db.create_table('food')
db.add_data('exercise', '2022-01-01', 'Ran 5 miles')
db.add_data('food', '2022-01-01', 'Ate a salad')
db.delete_table('exercise')