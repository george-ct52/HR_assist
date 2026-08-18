"""
Creates a sample SQLite employee database at data/employees.db.
Run this once before starting the app: `python seed_db.py`
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "employees.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS employees (
    employee_id   TEXT PRIMARY KEY,
    name          TEXT NOT NULL,
    department    TEXT NOT NULL,
    manager_name  TEXT,
    salary        INTEGER NOT NULL,
    joining_date  TEXT NOT NULL,
    leave_balance INTEGER NOT NULL
);
"""

SAMPLE_ROWS = [
    ("E1001", "George Kutty",     "Engineering", "Priya Nair",     1350000, "2021-03-15", 8),
    ("E1002", "Priya Nair",       "Engineering", "Anil Sharma",    2100000, "2018-06-01", 12),
    ("E1003", "Anil Sharma",      "Engineering", None,             3200000, "2015-01-10", 15),
    ("E1004", "Divya Menon",      "HR",          "Rahul Verma",    980000,  "2022-09-01", 5),
    ("E1005", "Rahul Verma",      "HR",          "Anil Sharma",    1750000, "2017-11-20", 10),
    ("E1006", "Karthik Iyer",     "Sales",       "Sneha Reddy",    1120000, "2023-02-14", 3),
    ("E1007", "Sneha Reddy",      "Sales",       "Anil Sharma",    2000000, "2016-07-07", 18),
    ("E1008", "Farah Sheikh",     "Finance",     "Rahul Verma",    1450000, "2020-05-05", 7),
]


def seed():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(SCHEMA)
    cur.execute("DELETE FROM employees")
    cur.executemany(
        "INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?)", SAMPLE_ROWS
    )
    conn.commit()
    conn.close()
    print(f"Seeded {len(SAMPLE_ROWS)} employees into {DB_PATH}")


if __name__ == "__main__":
    seed()
