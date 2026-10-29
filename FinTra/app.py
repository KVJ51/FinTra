from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import sqlite3
import os
import re
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fintra_super_secret_fintech_key_2026')

# ---------------------------------------------------------
# Database Utility Functions
# ---------------------------------------------------------
DB_FILE = 'fintra.db'

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def safe_float(val, default=0.0):
    if val is None or val == '':
        return default
    try:
        if isinstance(val, (int, float)):
            return float(val)
        cleaned = str(val).replace(',', '').replace('₹', '').replace('$', '').strip()
        return float(cleaned)
    except (ValueError, TypeError):
        return default

def initialize_db():
    conn = get_db()
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
    conn.commit()
    conn.close()

# ---------------------------------------------------------
# Gemini AI Configuration & Fallback Financial Expert Agent
# ---------------------------------------------------------
api_key = os.getenv('GENAI_API_KEY')
ai_model = None

if api_key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        # Try finding a working model
        for candidate in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]:
            try:
                ai_model = genai.GenerativeModel(candidate)
                print(f"DEBUG: Successfully initialized AI Model: {candidate}")
                break
            except Exception as e:
                print(f"DEBUG: Model {candidate} unavailable: {e}")
    except Exception as e:
        print(f"DEBUG: GenAI Initialization exception: {e}")

class FinTraFinancialExpertAgent:
    """
    Autonomous Financial Expert Agent.
    Provides expert guidance on accounting, financial metrics, MSME health,
    tax compliance, and audits if the Gemini API key is offline or unconfigured.
    """
    @staticmethod
    def answer_query(question: str, session_context: dict = None) -> str:
        q = question.lower()
        
        # 1. Contextual project data check
        if any(term in q for term in ["my business", "my company", "my report", "my profit", "my margin", "audit"]):
            if session_context and session_context.get('sales'):
                sales = safe_float(session_context.get('sales', 0))
                net_profit = safe_float(session_context.get('net_profit', 0))
                margin = (net_profit / sales * 100) if sales else 0
                return (
                    f"📊 **Financial Audit for {session_context.get('business_name', 'Your Business')}**:\n"
                    f"- **Recorded Sales**: ₹{sales:,.2f}\n"
                    f"- **Net Profit**: ₹{net_profit:,.2f}\n"
                    f"- **Net Profit Margin**: {margin:.1f}%\n\n"
                    f"**Expert Advisory**: {'Your profit margin is healthy (>15%). Focus on scaling sales while controlling overheads.' if margin >= 15 else 'Your net margin is under 15%. Recommend reviewing production costs and vendor agreements to reduce direct expenses.'}"
                )

        # 2. Working Capital & Liquidity
        if "working capital" in q:
            return (
                "💼 **Working Capital Analysis**:\n"
                "Working Capital = Current Assets - Current Liabilities. It measures your company's short-term operational liquidity.\n\n"
                "• **Positive Working Capital**: Indicates you can comfortably cover daily operations, inventory replenishment, and payroll.\n"
                "• **Negative Working Capital**: Signals cash flow strain and a need to accelerate accounts receivable collection or negotiate extended supplier credit terms."
            )

        # 3. Current Ratio / Liquidity Ratio
        if "current ratio" in q or "liquidity" in q:
            return (
                "📈 **Current Ratio Benchmark**:\n"
                "Current Ratio = Current Assets ÷ Current Liabilities.\n\n"
                "• **Optimal Target**: 1.5 to 2.0. This means you possess ₹1.50 to ₹2.00 of liquid resources for every ₹1.00 of near-term liability.\n"
                "• **Below 1.0**: Indicates high liquidity risk.\n"
                "• **Above 3.0**: May signify unproductively idle cash or excess stagnant inventory."
            )

        # 4. Debt to Equity & Solvency
        if "debt to equity" in q or "leverage" in q or "solvency" in q or "loans" in q:
            return (
                "⚖️ **Debt-to-Equity (D/E) Ratio**:\n"
                "D/E Ratio = Total Debt (Term Loans + Borrowings) ÷ Promoters Equity.\n\n"
                "• **Standard Benchmark**: Under 2.0 for manufacturing/MSMEs, under 1.0 for services/tech.\n"
                "• A high D/E ratio increases interest burden during slow economic quarters. Prioritize retiring high-interest short-term debt first."
            )

        # 5. Profit Margin & Pricing
        if "profit margin" in q or "improve margin" in q or "gross profit" in q or "net profit" in q:
            return (
                "🎯 **Strategies to Enhance Profit Margins**:\n"
                "1. **Direct Cost Optimization**: Renegotiate raw material bulk rates or production costs (COGS).\n"
                "2. **Value-Based Pricing**: Adjust prices by 3-5% on premium offerings; customers are often far less price-sensitive to value additions.\n"
                "3. **Eliminate Low-Margin SKU Leaks**: Review high-overhead, low-return product lines and reallocate marketing budget to top 20% profitable services."
            )

        # 6. Balance Sheet Golden Rule
        if "balance sheet" in q or "accounting equation" in q or "assets" in q or "liabilities" in q:
            return (
                "📑 **The Golden Accounting Equation**:\n"
                "**Total Assets = Total Liabilities + Owner's Equity**.\n\n"
                "Every rupee invested into the business (promoter capital or loan liability) must manifest as an asset (cash, equipment, inventory, or receivables). If your balance sheet does not reconcile to zero variance, verify accrued receivables or unpaid vendor dues."
            )

        # 7. Cash Flow vs Profit
        if "cash flow" in q or "cash" in q:
            return (
                "💰 **Cash Flow vs. Accounting Profit**:\n"
                "Profit on paper does not equal cash in the bank! A business can be profitable while suffering insolvency if receivables remain uncollected.\n\n"
                "• Implement strict 30-day payment terms.\n"
                "• Offer 2% early-payment discounts to customers.\n"
                "• Maintain a cash reserve equal to 3 months of baseline operating expenses."
            )

        # 8. General Financial Assistant
        return (
            "🏦 **FinTra Financial Advisory Overview**:\n"
            f"You asked: *\"{question}\"*\n\n"
            "As your dedicated financial companion, FinTra provides comprehensive balance sheet auditing, P&L analytics, and cash flow management for small enterprises.\n\n"
            "**Key Recommendations**:\n"
            "• Monitor your Current Ratio (target 1.5 - 2.0)\n"
            "• Keep Net Margin above 15% through lean cost control\n"
            "• Ensure your Balance Sheet satisfies: Assets = Liabilities + Equity\n"
            "You can complete the 3-step Financial Filing Wizard to generate a full diagnostic audit!"
        )

# ---------------------------------------------------------
# Helper Financial Metrics Computation
# ---------------------------------------------------------
def calculate_financial_health(project_data, balance_data, profit_loss_data):
    # Assets breakdown
    fixed_assets = safe_float(balance_data.get('fixed_assets', 0))
    cash = safe_float(balance_data.get('cash', 0))
    receivables = safe_float(balance_data.get('receivables', 0))
    stock = safe_float(balance_data.get('stock', 0))
    current_assets = safe_float(balance_data.get('current_assets', 0))
    if current_assets == 0:
        current_assets = cash + receivables + stock
    total_assets = fixed_assets + current_assets

    # Liabilities breakdown
    current_liabilities = safe_float(balance_data.get('current_liabilities', 0))
    long_term_liabilities = safe_float(balance_data.get('long_term_liabilities', 0))
    loans = safe_float(balance_data.get('term_loan', balance_data.get('loans', 0)))
    total_liabilities = current_liabilities + long_term_liabilities + loans

    # Equity
    promoters_capital = safe_float(balance_data.get('promoters_capital', balance_data.get('equity', 0)))
    total_equity_and_liabilities = total_liabilities + promoters_capital

    # Profit & Loss
    sales = safe_float(profit_loss_data.get('sales', 0))
    production_cost = safe_float(profit_loss_data.get('production_cost', 0))
    salary = safe_float(profit_loss_data.get('salary', 0))
    overheads = safe_float(profit_loss_data.get('overheads', 0))
    other_expenses = safe_float(profit_loss_data.get('other_expenses', 0))
    total_expenses = production_cost + salary + overheads + other_expenses

    gross_profit = safe_float(profit_loss_data.get('gross_profit', sales - production_cost))
    net_profit = safe_float(profit_loss_data.get('net_profit', gross_profit - (salary + overheads + other_expenses)))

    # Real Financial Ratios
    net_profit_margin = (net_profit / sales * 100) if sales > 0 else 0.0
    gross_profit_margin = (gross_profit / sales * 100) if sales > 0 else 0.0
    roa = (net_profit / total_assets * 100) if total_assets > 0 else 0.0
    roe = (net_profit / promoters_capital * 100) if promoters_capital > 0 else 0.0
    current_ratio = (current_assets / current_liabilities) if current_liabilities > 0 else (2.0 if current_assets > 0 else 1.0)
    debt_to_equity = (loans / promoters_capital) if promoters_capital > 0 else 0.0
    working_capital = current_assets - current_liabilities
    balance_variance = total_assets - total_equity_and_liabilities
    is_balanced = abs(balance_variance) < 1.0

    # Calculate overall health score (0 - 100)
    score = 50
    if is_balanced: score += 15
    if net_profit_margin >= 15: score += 15
    elif net_profit_margin > 0: score += 8
    if 1.3 <= current_ratio <= 2.5: score += 10
    elif current_ratio >= 1.0: score += 5
    if working_capital > 0: score += 5
    if debt_to_equity <= 2.0: score += 5
    score = min(max(score, 10), 100)

    return {
        'fixed_assets': fixed_assets,
        'current_assets': current_assets,
        'cash': cash,
        'receivables': receivables,
        'stock': stock,
        'total_assets': total_assets,
        'current_liabilities': current_liabilities,
        'long_term_liabilities': long_term_liabilities,
        'loans': loans,
        'total_liabilities': total_liabilities,
        'promoters_capital': promoters_capital,
        'total_equity_and_liabilities': total_equity_and_liabilities,
        'sales': sales,
        'production_cost': production_cost,
        'salary': salary,
        'overheads': overheads,
        'other_expenses': other_expenses,
        'total_expenses': total_expenses,
        'gross_profit': gross_profit,
        'net_profit': net_profit,
        'net_profit_margin': round(net_profit_margin, 2),
        'gross_profit_margin': round(gross_profit_margin, 2),
        'roa': round(roa, 2),
        'roe': round(roe, 2),
        'current_ratio': round(current_ratio, 2),
        'debt_to_equity': round(debt_to_equity, 2),
        'working_capital': round(working_capital, 2),
        'balance_variance': round(balance_variance, 2),
        'is_balanced': is_balanced,
        'health_score': score
    }

# ---------------------------------------------------------
# Application Routes
# ---------------------------------------------------------

@app.route('/')
def index():
    """
    Home page featuring the user's signature FinTra launcher card 
    (as shown in the provided photo) with smooth animations and quick financial stats.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    tx_count = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type='income'")
    total_income = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type='expense'")
    total_expense = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports")
    report_count = cursor.fetchone()[0]
    conn.close()

    net_balance = total_income - total_expense

    return render_template(
        'index.html',
        tx_count=tx_count,
        total_income=total_income,
        total_expense=total_expense,
        net_balance=net_balance,
        report_count=report_count
    )

@app.route('/dashboard')
def dashboard():
    """
    Comprehensive business dashboard:
    Monthly Income & Expense breakdown, recent transaction ledger, and metrics.
    """
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions ORDER BY date DESC, id DESC LIMIT 50")
    transactions = cursor.fetchall()

    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type='income'")
    total_income = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type='expense'")
    total_expense = cursor.fetchone()[0]

    net_balance = total_income - total_expense

    # Expense category distribution for Chart.js
    cursor.execute("""
        SELECT category, SUM(amount) as cat_total 
        FROM transactions 
        WHERE type='expense' 
        GROUP BY category 
        ORDER BY cat_total DESC
    """)
    expense_categories = cursor.fetchall()
    conn.close()

    cat_labels = [row['category'] for row in expense_categories]
    cat_values = [float(row['cat_total']) for row in expense_categories]

    return render_template(
        'dashboard.html',
        transactions=transactions,
        total_income=total_income,
        total_expense=total_expense,
        net_balance=net_balance,
        cat_labels=cat_labels,
        cat_values=cat_values
    )

@app.route('/add-income', methods=['GET', 'POST'])
def add_income():
    """Record a business income transaction."""
    if request.method == 'POST':
        source = request.form.get('source', '').strip()
        category = request.form.get('category', 'General Income').strip()
        amount = safe_float(request.form.get('amount'))
        date = request.form.get('date', datetime.today().strftime('%Y-%m-%d'))
        notes = request.form.get('notes', '').strip()

        if source and amount > 0:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO transactions (type, category, source_payee, amount, date, notes)
                VALUES ('income', ?, ?, ?, ?, ?)
            ''', (category, source, amount, date, notes))
            conn.commit()
            conn.close()
            return redirect(url_for('dashboard'))

    # Retrieve recent incomes to display on page
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE type='income' ORDER BY id DESC LIMIT 5")
    recent_incomes = cursor.fetchall()
    conn.close()

    return render_template('add_income.html', recent_incomes=recent_incomes)

@app.route('/add-expense', methods=['GET', 'POST'])
def add_expense():
    """Record a business expense transaction."""
    if request.method == 'POST':
        payee = request.form.get('category', '').strip()  # In old form, payee or category
        source_payee = request.form.get('source_payee', payee).strip()
        category = request.form.get('category_select', payee).strip()
        amount = safe_float(request.form.get('amount'))
        date = request.form.get('date', datetime.today().strftime('%Y-%m-%d'))
        notes = request.form.get('notes', '').strip()

        if (source_payee or category) and amount > 0:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO transactions (type, category, source_payee, amount, date, notes)
                VALUES ('expense', ?, ?, ?, ?, ?)
            ''', (category or 'General Expense', source_payee or category, amount, date, notes))
            conn.commit()
            conn.close()
            return redirect(url_for('dashboard'))

    # Retrieve recent expenses to display on page
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE type='expense' ORDER BY id DESC LIMIT 5")
    recent_expenses = cursor.fetchall()
    conn.close()

    return render_template('add_expense.html', recent_expenses=recent_expenses)

@app.route('/transactions/delete/<int:tx_id>', methods=['POST'])
def delete_transaction(tx_id):
    """Delete a transaction by ID."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

# ---------------------------------------------------------
# Unified Financial Filing Wizard (In-Step Direct Analysis)
# ---------------------------------------------------------

@app.route('/project-report', methods=['GET', 'POST'])
@app.route('/financial-analysis', methods=['GET', 'POST'])
def project_report():
    """Unified In-Step Financial Wizard: Business Profile, Balance Sheet & P&L."""
    if request.method == 'POST':
        form = request.form

        # 1. Business Profile (Step 1)
        project_report_data = {
            'business_name': form.get('business_name', '').strip() or 'My Business Enterprise',
            'place': form.get('place', '').strip() or 'Headquarters',
            'incorporation_date': form.get('incorporation_date', '').strip() or datetime.today().strftime('%Y-%m-%d'),
            'business_start_date': form.get('business_start_date', '').strip() or datetime.today().strftime('%Y-%m-%d'),
            'team_leader': form.get('team_leader', '').strip() or 'Managing Director',
            'admin': form.get('admin', '').strip() or 'Administration Head',
            'production': form.get('production', '').strip(),
            'supply_chain': form.get('supply_chain', '').strip(),
            'marketing': form.get('marketing', '').strip(),
            'maintenance': form.get('maintenance', '').strip()
        }

        # 2. Balance Sheet (Step 2)
        balance_sheet_data = {
            'fixed_assets': form.get('fixed_assets', '0'),
            'cash': form.get('cash', '0'),
            'receivables': form.get('receivables', '0'),
            'stock': form.get('stock', '0'),
            'promoters_capital': form.get('promoters_capital', '0'),
            'term_loan': form.get('term_loan', '0'),
            'current_liabilities': form.get('current_liabilities', '0'),
            'long_term_liabilities': form.get('long_term_liabilities', '0')
        }

        # 3. Profit & Loss (Step 3)
        profit_loss_data = {
            'sales': form.get('sales', '0'),
            'production_cost': form.get('production_cost', '0'),
            'salary': form.get('salary', '0'),
            'overheads': form.get('overheads', '0'),
            'other_expenses': form.get('other_expenses', '0'),
            'gross_profit': form.get('gross_profit', '0'),
            'net_profit': form.get('net_profit', '0')
        }

        session['project_report'] = project_report_data
        session['balance_sheet'] = balance_sheet_data
        session['profit_loss'] = profit_loss_data

        return redirect(url_for('result_summary'))

    project_data = session.get('project_report', {})
    balance_data = session.get('balance_sheet', {})
    profit_loss_data = session.get('profit_loss', {})
    initial_step = request.args.get('step', '1')

    return render_template(
        'project_report.html',
        project_data=project_data,
        balance_data=balance_data,
        profit_loss_data=profit_loss_data,
        initial_step=initial_step
    )

@app.route('/balance-sheet', methods=['GET', 'POST'])
def balance_sheet():
    """Direct shortcut into Step 2 (Balance Sheet) of the unified wizard."""
    if request.method == 'POST':
        session['balance_sheet'] = request.form.to_dict()
        return redirect(url_for('project_report', step=3))
    return redirect(url_for('project_report', step=2))

@app.route('/profit-loss', methods=['GET', 'POST'])
def profit_loss():
    """Direct shortcut into Step 3 (Profit & Loss) of the unified wizard."""
    if request.method == 'POST':
        session['profit_loss'] = request.form.to_dict()
        return redirect(url_for('result_summary'))
    return redirect(url_for('project_report', step=3))

@app.route('/result-summary', methods=['GET', 'POST'])
def result_summary():

    """
    Step 4: Final Comprehensive Financial Audit & Executive Summary.
    Calculates accurate business ratios and saves the completed report.
    """
    project_data = session.get('project_report', {})
    balance_data = session.get('balance_sheet', {})
    profit_loss_data = session.get('profit_loss', {})

    # Compute complete metrics
    metrics = calculate_financial_health(project_data, balance_data, profit_loss_data)

    # Persist record into reports table if business name is provided
    if project_data.get('business_name'):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO reports (
                    business_name, incorporation_date, business_start_date, place,
                    team_leader, admin, production, supply_chain, marketing, maintenance,
                    fixed_assets, current_assets, current_liabilities, long_term_liabilities,
                    equity, loans, promoters_capital, cash, receivables, stock,
                    gross_profit, net_profit, production_cost, sales, salary,
                    overheads, other_expenses
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                project_data.get('business_name'),
                project_data.get('incorporation_date'),
                project_data.get('business_start_date'),
                project_data.get('place'),
                project_data.get('team_leader'),
                project_data.get('admin'),
                project_data.get('production'),
                project_data.get('supply_chain'),
                project_data.get('marketing'),
                project_data.get('maintenance'),
                metrics['fixed_assets'],
                metrics['current_assets'],
                metrics['current_liabilities'],
                metrics['long_term_liabilities'],
                metrics['promoters_capital'],
                metrics['loans'],
                metrics['promoters_capital'],
                metrics['cash'],
                metrics['receivables'],
                metrics['stock'],
                metrics['gross_profit'],
                metrics['net_profit'],
                metrics['production_cost'],
                metrics['sales'],
                metrics['salary'],
                metrics['overheads'],
                metrics['other_expenses']
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            print("Database report insert error:", e)

    return render_template(
        'result_summary.html',
        project_data=project_data,
        balance_data=balance_data,
        profit_loss_data=profit_loss_data,
        metrics=metrics
    )

@app.route('/load-demo-data')
def load_demo_data():
    """Populates realistic business financials into session for instant testing."""
    session['project_report'] = {
        'business_name': 'QuantumTech Dynamics Ltd.',
        'incorporation_date': '2024-03-15',
        'business_start_date': '2024-06-01',
        'place': 'Bangalore, Tech Zone 4',
        'team_leader': 'Arjun Mehta (CEO)',
        'admin': 'Kavita Rao (Operations VP)',
        'production': 'Lead Architect Rajesh K.',
        'supply_chain': 'Logistics Pro Anita S.',
        'marketing': 'Growth Specialist Priya V.',
        'maintenance': 'Ops Engineering Group'
    }

    session['balance_sheet'] = {
        'promoters_capital': '500000',
        'term_loan': '300000',
        'current_liabilities': '150000',
        'fixed_assets': '450000',
        'cash': '180000',
        'receivables': '160000',
        'stock': '160000'
    }

    session['profit_loss'] = {
        'sales': '1250000',
        'production_cost': '520000',
        'overheads': '110000',
        'salary': '280000',
        'other_expenses': '45000',
        'gross_profit': '730000',
        'net_profit': '295000'
    }

    return redirect(url_for('result_summary'))

@app.route('/reset-data')
def reset_data():
    """Clear session data and start fresh."""
    session.pop('project_report', None)
    session.pop('balance_sheet', None)
    session.pop('profit_loss', None)
    return redirect(url_for('project_report'))

# ---------------------------------------------------------
# Chatbot & AI Financial Advisor Endpoints
# ---------------------------------------------------------

@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')

@app.route('/ask-financial', methods=['POST'])
def ask_financial():
    try:
        data = request.get_json(force=True, silent=True) or {}
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"answer": "Please enter a financial or accounting question."}), 400

        # Gather active financial context if available
        active_context = {
            'business_name': session.get('project_report', {}).get('business_name', 'Your Business'),
            'sales': session.get('profit_loss', {}).get('sales', 0),
            'net_profit': session.get('profit_loss', {}).get('net_profit', 0)
        }

        # Attempt Gemini API first if configured
        if api_key and ai_model:
            try:
                system_prompt = (
                    "You are FinTra's Senior Financial & Accounting Advisor. "
                    "Provide practical, concise, high-value financial advice tailored to small businesses, "
                    "startups, and MSMEs in 3 to 4 clear paragraphs with bullet points. "
                    f"User's Question: {question}"
                )
                response = ai_model.generate_content(system_prompt)
                if response and hasattr(response, 'text') and response.text.strip():
                    return jsonify({"answer": response.text.strip()})
            except Exception as api_err:
                print(f"DEBUG: GenAI runtime exception: {api_err}. Falling back to internal FinTra Expert Agent.")

        # Fallback: Autonomous FinTra Expert Agent
        fallback_answer = FinTraFinancialExpertAgent.answer_query(question, active_context)
        return jsonify({"answer": fallback_answer})

    except Exception as e:
        print(f"Error in ask_financial: {e}")
        return jsonify({"answer": "I encountered an issue processing your request. Please ask your question again."})

# ---------------------------------------------------------
# Run Application
# ---------------------------------------------------------
if __name__ == '__main__':
    initialize_db()
    app.run(debug=True, port=5000)