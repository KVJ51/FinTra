import sqlite3

def init_database():
    conn = sqlite3.connect('fintra.db')
    cursor = conn.cursor()

    # Reports Table: Stores complete business reports, balance sheets, and P&L
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
            fixed_assets REAL DEFAULT 0,
            current_assets REAL DEFAULT 0,
            current_liabilities REAL DEFAULT 0,
            long_term_liabilities REAL DEFAULT 0,
            equity REAL DEFAULT 0,
            loans REAL DEFAULT 0,
            promoters_capital REAL DEFAULT 0,
            cash REAL DEFAULT 0,
            receivables REAL DEFAULT 0,
            stock REAL DEFAULT 0,
            gross_profit REAL DEFAULT 0,
            net_profit REAL DEFAULT 0,
            production_cost REAL DEFAULT 0,
            sales REAL DEFAULT 0,
            salary REAL DEFAULT 0,
            overheads REAL DEFAULT 0,
            other_expenses REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Transactions Table: Stores individual Income and Expense transactions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT CHECK(type IN ('income', 'expense')),
            category TEXT NOT NULL,
            source_payee TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Add sample transaction data if empty for instant out-of-the-box experience
    cursor.execute('SELECT COUNT(*) FROM transactions')
    if cursor.fetchone()[0] == 0:
        sample_transactions = [
            ('income', 'Product Sales', 'Client Alpha Enterprise', 125000.00, '2026-10-25', 'Monthly software license fee'),
            ('income', 'Consulting', 'Delta Corp', 45000.00, '2026-10-26', 'Financial advisory retainer'),
            ('expense', 'Salaries', 'Staff Payroll', 65000.00, '2026-10-27', 'October payroll disbursement'),
            ('expense', 'Office Rent', 'Skyline Realty', 20000.00, '2026-10-27', 'Monthly coworking & utilities'),
            ('expense', 'Cloud Hosting', 'AWS & Cloudflare', 7500.00, '2026-10-28', 'Server infrastructure'),
            ('income', 'Services', 'Omega Logistics', 38000.00, '2026-10-28', 'API integration project payment'),
            ('expense', 'Marketing', 'Google & Meta Ads', 12000.00, '2026-10-28', 'Q4 customer acquisition campaign')
        ]
        cursor.executemany('''
            INSERT INTO transactions (type, category, source_payee, amount, date, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_transactions)

    conn.commit()
    conn.close()
    print("Database initialized with reports and transactions tables successfully.")

if __name__ == '__main__':
    init_database()
