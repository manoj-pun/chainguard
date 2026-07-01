# ChainGuard
 
ChainGuard is a digital chain-of-custody evidence management system built for law enforcement workflows. It tracks evidence from collection through analysis to court submission, with a fully auditable trail at every step.
 
This project is built with **Django REST Framework**, designed with production-grade architecture patterns rather than a typical CRUD tutorial approach.

## Overview
 
Chain of custody is critical in law enforcement — every piece of evidence needs a verifiable, tamper-evident trail showing who handled it, when, and what happened to it. ChainGuard models this as a real system: cases and evidence move through defined lifecycles, every meaningful action is logged immutably, and access is tightly scoped by role.

## Key Features
 
- **Role-based access control** — Officer, Supervisor, Storage Clerk, Analyst, and Pending roles, each with scoped permissions
- **Case & evidence lifecycle management** — full state machines governing valid transitions
- **Immutable audit logging** — every action on a case or piece of evidence is recorded as a permanent chain-of-custody record
- **File integrity verification** — SHA-256 hashing of uploaded evidence files
- **PDF export** — generate official audit log reports for cases
- **Versioned findings** — analyst findings are versioned rather than overwritten, preserving history
- **Race-condition-safe operations** — row-level locking on critical operations like badge ID generation and case updates
- **JWT authentication** — access tokens in memory, refresh tokens in httpOnly cookies, with silent token refresh

### Lifecycles
 
  **Case status flow:**
  ```
  OPEN → SUBMITTED_TO_STORAGE → IN_STORAGE → WITH_ANALYST → UNDER_REVIEW → SENT_TO_COURT → CLOSED
  ```
 
  **Evidence status flow:**
  ```
  COLLECTED → IN_STORAGE → WITH_ANALYST → ANALYSIS_COMPLETE
  ```
 
Both are implemented as explicit state machines with guarded transitions — evidence and cases can't skip steps or move backward without going through defined rules.

## Roles & Permissions

| Role           | Access                                                        |
|-----------------|----------------------------------------------------------------|
| Supervisor      | Review and approve case transitions, oversee all cases, assign roles to pending users *(auto-assigned to Django superusers)* |
| Officer         | Create cases, submit evidence                                 |
| Storage Clerk   | Manage evidence intake and storage status                     |
| Analyst         | Submit findings, update evidence to analysis-complete           |
| Pending         | No access until a role is assigned by a supervisor              |

## Project Structure
```
.
├── apps
│   ├── audits
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── templates
│   │   │   └── audits
│   │   ├── tests.py
│   │   └── views.py
│   ├── cases
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── common
│   │   └── permissions.py
│   ├── findings
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── templates
│   │   │   └── findings
│   │   │       └── finding_pdf.html
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── users
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── serializers.py
│       ├── services.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── README.md
└── requirements.txt
```

## Getting Started
 
### Prerequisites
 
- Python 3.10+
- PostgreSQL
- pip
### PostgreSQL Setup
 
1. Make sure PostgreSQL is installed and running on your machine.
   - **Mac:** `brew install postgresql` then `brew services start postgresql`
   - **Linux:** `sudo apt install postgresql postgresql-contrib` then `sudo service postgresql start`
   - **Windows:** install via the [official installer](https://www.postgresql.org/download/windows/)
  

2. Open the PostgreSQL shell:
```bash
   psql -U postgres
```
 
3. Create a database and user for the project:
```sql
   CREATE DATABASE chainguard;
   CREATE USER chainguard_user WITH PASSWORD 'your_password';
   ALTER ROLE chainguard_user SET client_encoding TO 'utf8';
   ALTER ROLE chainguard_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE chainguard_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE chainguard TO chainguard_user;
```
 
4. Exit the shell (`\q`) and update your `.env` file to match the credentials you created:
```env
   DB_NAME=chainguard
   DB_USER=chainguard_user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
```

### Installation
 
1. Clone the repository
```bash
   git clone https://github.com/<your-username>/chainguard.git
   cd chainguard/chainguard_backend
```
 
2. Create and activate a virtual environment
```bash
   python -m venv venv
   source venv/bin/activate      # Mac/Linux
   venv\Scripts\activate         # Windows
```
 
3. Install dependencies
```bash
   pip install -r requirements.txt
```
 
4. Set up environment variables (see below)
5. Make sure your PostgreSQL database and user are created (see PostgreSQL Setup above) and your `.env` file has the matching `DB_*` values
6. Run migrations
```bash
   python manage.py migrate
```
 
7. Create a superuser
```bash
   python manage.py createsuperuser
```
   > Creating a superuser automatically assigns the **SUPERVISOR** role, giving full access to case review, approvals, and role management right out of the box.
 
8. Run the development server
```bash
   python manage.py runserver
```
 
9. API will be available at `http://127.0.0.1:8000`
### Environment Variables
 
Create a `.env` file in the project root:
 
```env
DEBUG=True
SECRET_KEY=your_django_secret_key
 
DB_NAME=chainguard
DB_USER=chainguard_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```


## License
 
This project is for educational/portfolio purposes.