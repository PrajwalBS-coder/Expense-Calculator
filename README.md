# Expense Calculator

A personal expense tracker with a Django REST API and a Svelte dashboard. The current product focuses on recording and understanding expenses in Indian rupees. Income tracking is kept in the backend for a future phase.

## Current Features

- JWT registration, login, token refresh, and logout flow
- User-owned expense and category CRUD operations
- Search and sort expenses by title, date, or amount
- Recurring expense schedules with weekly, monthly, and yearly frequencies
- Monthly expense summaries, category breakdowns, and budget comparisons
- Expense-only Svelte dashboard with INR formatting
- CORS support for local frontend development

## Project Structure

```text
Expense Calculator/
├── E_Calculator/                 # Django project and backend apps
│   ├── E_Calculator/             # Settings, URLs, ASGI, and WSGI
│   ├── common/                   # Shared models and utilities
│   ├── expenses/                 # Expense domain, APIs, reports, migrations
│   ├── users/                    # Custom user model and auth APIs
│   ├── manage.py
│   └── build.sh
├── fe/                           # Svelte + Vite frontend
│   ├── src/App.svelte            # Auth and dashboard UI
│   ├── src/api.js                # API client and JWT refresh logic
│   ├── src/styles.css
│   └── package.json
├── requirements.txt
├── render.yaml
└── README.md
```

## Technology Stack

- **Frontend:** Svelte, Vite, JavaScript
- **Backend:** Django 6, Django REST Framework
- **Authentication:** Simple JWT
- **Database:** PostgreSQL by default, with `DATABASE_URL` override support
- **Deployment:** Render configuration included in `render.yaml`

## Local Setup

### Prerequisites

- Python 3.11+
- Node.js and npm
- PostgreSQL, or a configured `DATABASE_URL`

### Backend

From the repository root:

```bash
python -m venv expense_calculator
```

Windows:

```powershell
.\expense_calculator\Scripts\activate
```

macOS/Linux:

```bash
source expense_calculator/bin/activate
```

Install dependencies and run migrations:

```bash
pip install -r requirements.txt
cd E_Calculator
python manage.py migrate
python manage.py runserver
```

The API runs at `http://127.0.0.1:8000/`.

### Frontend

Open a second terminal from the repository root:

```bash
cd fe
npm install
npm run dev
```

The Vite development server normally runs at `http://localhost:5173/`. If that port is occupied, Vite may choose another port. The backend allows local ports `5173`, `5174`, and `5175` for both `localhost` and `127.0.0.1`.

To use another API URL, create `fe/.env`:

```env
VITE_API_URL=http://127.0.0.1:8000/api
```

## Environment Variables

The backend supports these settings through environment variables:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://user:password@localhost:5432/expense_calculator
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

For production, use a strong secret key, set `DEBUG=False`, configure the deployed frontend origin, and provide a production database URL.

## API Route Groups

- `POST /api/users/create/` - register a user
- `POST /api/users/login/` - obtain access and refresh tokens
- `POST /api/users/refresh/` - refresh an access token
- `/api/expenses/categories/` - expense categories
- `/api/expenses/expenses/` - expense records
- `/api/expenses/recurring-expenses/` - recurring expense schedules
- `/api/expenses/budgets/` - budgets
- `/api/expenses/reports/` - monthly, category, and budget reports
- `/swagger/` and `/redoc/` - API documentation

Authenticated expense requests require:

```http
Authorization: Bearer <access-token>
```

## Testing

Run the backend checks and tests from `E_Calculator`:

```bash
python manage.py check
python manage.py test expenses.tests users.test_api
```

Build the frontend:

```bash
cd ../fe
npm run build
```

## Roadmap

- [x] User authentication
- [x] Expense and category CRUD
- [x] Search and sorting
- [x] Recurring expenses
- [x] Monthly reports and budget comparisons
- [ ] Full expense management screens
- [ ] Budget alerts and limits validation
- [ ] Income tracking and income reports
- [ ] Charts and richer dashboard visualizations
