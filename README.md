# 💼 FinTra: AI-Powered Auditing & Finance Tracing System  

FinTra is an intelligent financial management solution designed to **simplify, automate, and visualize** the financial status of an organization.  

By automating net profit calculation and tracking diverse expense streams, FinTra delivers **clear, data-driven insights** for efficient financial auditing and smarter decision-making.

---

## 🎯 Purpose  

The primary goal of FinTra is to streamline financial monitoring by:

- Calculating **Net Profits**
- Tracking key expense streams:
  - Sales
  - Salaries
  - Production Costs
  - Overheads
- Forecasting future trends using intelligent data handling

This ensures accurate auditing and improved financial transparency.

---

## 🚀 Key Features  

### 🔍 AI-Powered Auditing  
- Automated financial tracing  
- Detects inconsistencies in records  
- Pattern recognition-based validation  

### 💬 Interactive Chatbot  
- `chatbot.html` interface  
- Query financial data and reports  
- Instant financial insights  

### 📊 Comprehensive Dashboard  
- Real-time **Profit & Loss Visualization**  
- Balance Sheet Overview  
- Result Summaries  

### 🧾 Comprehensive Reporting  
- Generate:
  - Profit & Loss Statements  
  - Project Reports  
- Direct export from dashboard  

### 🗃️ Robust Data Management  
- Database initialization & maintenance scripts (`db_setup.py`)  
- Structured financial record storage  

### 📈 Automated Net Profit Calculation  
- Instant evaluation of financial health  

### 📊 Dynamic Visualizations  
- Bar Charts (Income vs Expenses)  
- Line Charts (Growth Analysis)  

### 🔮 Growth Forecasting  
- 6-Month forecast model  
- Income & Expense trend predictions  

---

## 🛠️ Tech Stack  

| Layer         | Technology Used |
|--------------|----------------|
| Backend      | Python (Flask) |
| Frontend     | HTML5, CSS3, JavaScript |
| Database     | SQLite (`fintra.db`) |
| AI Component | FinTra Bot with Pattern Recognition |

---

## 📦 Installation & Setup  

  

```bash
git clone https://github.com/KVJ51/FinTra.git
cd FinTra

Create a Virtual Environment:


python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Dependencies:

pip install -r requirements.txt
Environment Configuration:
Create a .env file in the root directory to store your API keys and secrets.

Initialize Database:

python db_setup.py

Run the App:

python app.py
