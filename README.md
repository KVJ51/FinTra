FinTra: AI-Powered Auditing & Finance Tracing System
FinTra is an intelligent financial management tool designed to streamline expense tracking and provide automated auditing insights. Built as part of a portfolio of AI and Machine Learning solutions, it leverages data-driven logic to help users maintain a clear view of their financial health.

🚀 Features
Automated Finance Tracing: Record and categorize income and expenses with ease.

AI Chatbot Integration: Interact with your financial data through a dedicated chatbot interface.

Comprehensive Reporting: Generate Profit & Loss statements and Project Reports directly from the dashboard.

Balance Sheet Visualization: View real-time summaries of assets and liabilities.

🛠️ Tech Stack
Backend: Python (Flask/FastAPI)

Frontend: HTML5, CSS3, JavaScript

Database: SQLite (fintra.db)

AI/ML: Integrated logic for auditing and hallucination detection

📋 Installation & Setup
Clone the repository:

Bash
git clone https://github.com/your-username/fintra.git
cd fintra
Set up a virtual environment:

Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

Bash
pip install -r requirements.txt
Configure Environment Variables:
Create a .env file in the root directory (refer to .env.example for required keys).

Initialize the Database:

Bash
python db_setup.py
Run the Application:

Bash
python app.py
📂 Project Structure
templates/: UI components including the Dashboard and AI Chatbot.

static/: Custom CSS and JavaScript for a polished UI/UX.

app.py: Main application logic and routing.

db_setup.py: Script to initialize local database schemas.
