import sqlite3

def query_employee_data(question, employee_id):

    conn = sqlite3.connect("data/employees.db")

    cursor = conn.cursor()

    
    cursor.execute(
        "SELECT * FROM employees WHERE employee_id = ?",
        (employee_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if not row:
        return "Employee not found."

    return row