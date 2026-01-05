# Expense Calculator

A web application to track and manage personal expenses efficiently.

## Features

- **Expense Tracking**: Log your daily expenses easily.
- **User Accounts**: Personalized experience with secure login (In Progress).
- **Dashboard**: View expense summaries and trends (Planned).

## Technology Stack

- **Backend**: Django (Python)
- **Database**: SQLite (Default)

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.8+ installed
- pip (Python package installer)

### Installation

1. **Navigate to the project directory:**

   ```bash
   cd "c:\Personal\Expense Calculator"
   ```

2. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install django
   ```

4. **Run Migrations:**

   ```bash
   cd E_Calculator
   python manage.py migrate
   ```

5. **Start the Development Server:**

   ```bash
   python manage.py runserver
   ```

   Access the application at `http://127.0.0.1:8000/`.

## Roadmap

- [ ] User Authentication (Login/Register)
- [ ] CRUD operations for Expenses
- [ ] Monthly Reports & Visualizations
