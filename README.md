# Expense Calculator

A web application to track and manage personal expenses efficiently.

## Features

- **Expense Tracking**: Log your daily expenses easily.
- **User Accounts**: Personalized experience with secure login (In Progress).
- **Dashboard**: View expense summaries and trends (Planned).

## Technology Stack

- **Backend**: Django (Python)
- **Database**: PostgreSQL by default, with support for `DATABASE_URL` override

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.11+
- pip (Python package installer)
- PostgreSQL database (or a configured `DATABASE_URL`)

### Installation

1. **Navigate to the project directory:**

   ```bash
   cd "c:\Personal\Expense Calculator"
   ```

2. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv expense_calculator
   # Windows
   .\expense_calculator\Scripts\activate
   # macOS/Linux
   source expense_calculator/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** for Django and the database if needed:

   ```bash
   export SECRET_KEY="your-secret-key"
   export DEBUG="True"
   export ALLOWED_HOSTS="localhost,127.0.0.1"
   export DATABASE_URL="postgres://user:password@localhost:5432/expense_calculator"
   ```

5. **Run Migrations:**

   ```bash
   cd E_Calculator
   python manage.py migrate
   ```

6. **Start the Development Server:**

   ```bash
   python manage.py runserver
   ```

   Access the application at `http://127.0.0.1:8000/`.

## Roadmap

- [ ] User Authentication (Login/Register)
- [ ] CRUD operations for Expenses
- [ ] Monthly Reports & Visualizations
