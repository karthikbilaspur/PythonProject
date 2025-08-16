import sqlite3

class EmployeeDatabase:
    def __init__(self, database_name):
        self.database_name = database_name
        self.connection = sqlite3.connect(database_name)
        print(f"Connected to {database_name}")
        self.create_table()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            position TEXT,
                            salary REAL
                        )''')
        self.connection.commit()

    def insert_data(self, name, position, salary):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO employees (name, position, salary) VALUES (?, ?, ?)",
                       (name, position, salary))
        self.connection.commit()

    def update_salary(self, employee_id, new_salary):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE employees SET salary = ? WHERE id = ?",
                       (new_salary, employee_id))
        self.connection.commit()

    def query_data(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()

        print("\nEmployee Data:")
        for row in rows:
            print(
                f"ID: {row[0]}, Name: {row[1]}, Position: {row[2]}, Salary: {row[3]}")

    def delete_employee(self, employee_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM employees WHERE id = ?",
                       (employee_id,))
        self.connection.commit()

    def close_connection(self):
        self.connection.close()
        print(f"Connection to {self.database_name} closed.")


if __name__ == "__main__":
    database_name = "employee_database.db"

    db = EmployeeDatabase(database_name)

    db.insert_data("John Doe", "Software Engineer", 75000.0)
    db.insert_data("Jane Smith", "Data Analyst", 60000.0)

    print("\nAfter Insertions:")
    db.query_data()

    db.update_salary(1, 80000.0)

    print("\nAfter Update:")
    db.query_data()

    db.delete_employee(2)

    print("\nAfter Deletion:")
    db.query_data()

    db.close_connection()