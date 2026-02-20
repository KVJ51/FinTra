import sqlite3

conn = sqlite3.connect('fintra.db')
cursor = conn.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_name TEXT,
            incorporation_date TEXT,
            business_start_date TEXT,
            place TEXT,
            team_leader TEXT,
            admin TEXT,
            production TEXT,
            supply_chain TEXT,
            marketing TEXT,
            maintenance TEXT,
            fixed_assets REAL,
            current_assets REAL,
            current_liabilities REAL,
            long_term_liabilities REAL,
            equity REAL,
            loans REAL,
            gross_profit REAL,
            net_profit REAL,
            production_cost REAL,
            sales REAL,
            salary REAL,
            overheads REAL,
            other_expenses REAL
        )
    ''')

conn.commit()
conn.close()
