from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'fintra_secret'

# Configure your API key from environment variable (for security reasons)
api_key = os.getenv('GENAI_API_KEY')
if not api_key:
    print("WARNING: GENAI_API_KEY environment variable is not set!")
else:
    print(f"DEBUG: API Key configured successfully")

genai.configure(api_key=api_key)

# List available models and find one that works
available_model = None
try:
    print("DEBUG: Listing available models...")
    models = genai.list_models()
    for m in models:
        print(f"DEBUG: Available model: {m.name}")
        if "generateContent" in m.supported_generation_methods:
            available_model = m.name.replace("models/", "")
            print(f"DEBUG: Found suitable model: {available_model}")
            break
except Exception as e:
    print(f"DEBUG: Error listing models: {e}")

# Use the found model or fall back to specific ones
if available_model:
    print(f"DEBUG: Using detected model: {available_model}")
    try:
        model = genai.GenerativeModel(available_model)
    except Exception as e:
        print(f"DEBUG: Error with detected model: {e}, trying fallback...")
        available_model = None

if not available_model:
    # Try models in order of preference
    models_to_try = ["gemini-1.5-pro", "gemini-pro", "gemini-2.5-flash"]
    model = None
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            print(f"DEBUG: Successfully initialized {model_name}")
            break
        except Exception as e:
            print(f"DEBUG: {model_name} not available: {e}")
    
    if model is None:
        print("WARNING: No suitable model found!")
        model_name = "gemini-pro"  # Default fallback
        model = genai.GenerativeModel(model_name)
        print(f"DEBUG: Using default model: {model_name}")

def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add-income', methods=['GET', 'POST'])
def add_income():
    if request.method == 'POST':
        # Handle income addition logic here
        return redirect(url_for('index'))
    return render_template('add_income.html')

@app.route('/add-expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        # Handle expense addition logic here
        return redirect(url_for('index'))
    return render_template('add_expense.html')

@app.route('/project-report', methods=['GET', 'POST'])
def project_report():
    if request.method == 'POST':
        session['project_report'] = request.form.to_dict()
        return redirect(url_for('balance_sheet'))
    return render_template('project_report.html')

@app.route('/balance-sheet', methods=['GET', 'POST'])
def balance_sheet():
    if request.method == 'POST':
        session['balance_sheet'] = request.form.to_dict()
        return redirect(url_for('profit_loss'))
    return render_template('balance_sheet.html')

@app.route('/profit-loss', methods=['GET', 'POST'])
def profit_loss():
    if request.method == 'POST':
        session['profit_loss'] = request.form.to_dict()
        return redirect(url_for('result_summary'))
    return render_template('profit_loss.html')

@app.route('/result-summary')
def result_summary():
    project_data = session.get('project_report', {})
    balance_data = session.get('balance_sheet', {})
    profit_loss_data = session.get('profit_loss', {})

    total_liabilities = sum(safe_float(v) for k, v in balance_data.items() if 'liab' in k.lower())
    total_assets = sum(safe_float(v) for k, v in balance_data.items() if 'asset' in k.lower())
    gross_profit = safe_float(profit_loss_data.get('gross_profit'))
    net_profit_margin = (gross_profit / total_assets) * 100 if total_assets else 0

    allowed_columns = [
        'business_name', 'incorporation_date', 'business_start_date', 'place',
        'team_leader', 'admin', 'production', 'supply_chain', 'marketing', 'maintenance',
        'fixed_assets', 'current_assets', 'current_liabilities', 'long_term_liabilities',
        'equity', 'loans', 'gross_profit', 'net_profit', 'production_cost', 'sales', 'salary',
        'overheads', 'other_expenses'
    ]

    fields = {k: v for k, v in {**project_data, **balance_data, **profit_loss_data}.items() if k in allowed_columns}
    columns = ', '.join(fields.keys())
    placeholders = ', '.join(['?'] * len(fields))
    values = [
        safe_float(v) if isinstance(v, str) and v.replace('.', '', 1).isdigit() else v
        for v in fields.values()
    ]

    try:
        conn = sqlite3.connect('fintra.db')
        cursor = conn.cursor()
        cursor.execute(f'INSERT INTO reports ({columns}) VALUES ({placeholders})', values)
        conn.commit()
    except Exception as e:
        print("Database insert error:", e)
    finally:
        conn.close()

    return render_template(
        'result_summary.html',
        project_data=project_data,
        balance_data=balance_data,
        profit_loss_data=profit_loss_data,
        total_liabilities=total_liabilities,
        total_assets=total_assets,
        gross_profit=gross_profit,
        net_profit_margin=round(net_profit_margin, 2)
    )

def initialize_db():
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

@app.route("/chatbot")
def chatbot_page():
    return render_template("chatbot.html")

@app.route("/ask-financial", methods=["POST"])
def ask_financial():
    try:
        data = request.json
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"answer": "Please enter a valid question."}), 400

        if not api_key:
            return jsonify({"answer": "API key is not configured. Please set GENAI_API_KEY environment variable."}), 500

        # Create a more specific prompt for financial questions
        prompt = f"""You are a financial expert assistant. Answer this question clearly and concisely in 2-3 sentences.

Question: {question}

Provide practical, actionable advice about finance, business, accounting, budgeting, profit/loss analysis, balance sheets, or financial planning."""

        print(f"DEBUG: Preparing request for question: {question}")
        print(f"DEBUG: Using model: {model.model_name if hasattr(model, 'model_name') else 'unknown'}")
        
        # Generate content from the model
        response = model.generate_content(prompt)
        
        print(f"DEBUG: Response received successfully")
        
        # Check if response has text and is not blocked
        if response and hasattr(response, 'text'):
            answer_text = response.text
            if answer_text and answer_text.strip():
                print(f"DEBUG: Returning answer: {answer_text[:80]}...")
                return jsonify({"answer": answer_text.strip()})
            else:
                print(f"DEBUG: Response text is empty")
                return jsonify({"answer": "I couldn't generate a response. Please try rephrasing your question."})
        else:
            print(f"DEBUG: Response object invalid")
            return jsonify({"answer": "I couldn't generate a response. Please try again."})
            
    except Exception as e:
        error_msg = str(e)
        print(f"DEBUG: Exception in ask_financial - {type(e).__name__}: {error_msg}")
        import traceback
        print(traceback.format_exc())
        
        # Return specific error messages
        if "not found" in error_msg.lower() or "not supported" in error_msg.lower():
            return jsonify({"answer": "The AI model is not available. Please try again later."})
        elif "authentication" in error_msg.lower() or "invalid" in error_msg.lower():
            return jsonify({"answer": "API authentication error. Please check your configuration."})
        elif "quota" in error_msg.lower():
            return jsonify({"answer": "API quota exceeded. Please try again later."})
        else:
            return jsonify({"answer": "I encountered an error. Please try asking your question again."})

if __name__ == '__main__':
    initialize_db()
    app.run(debug=True)