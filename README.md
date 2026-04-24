## Author

Developed by: OllyCodes03  
GitHub: https://github.com/OllyCodes03

---

# Helpdesk System

A full-stack Flask-based Helpdesk Ticket Management System with user authentication, role-based access control, and admin dashboard. Deployed on Render with PostgreSQL.

---

## Live Demo
https://helpdesk-system-kpew.onrender.com

---

## Features

### User Features
- User registration & login system
- Create support tickets
- View personal tickets
- Track ticket status (Open / Closed)
- Secure session handling

### Admin Features
- Admin dashboard
- View all user tickets
- Update ticket status
- Manage users
- Promote users to admin

---

## Tech Stack

- Python 3
- Flask (Backend Framework)
- Flask-SQLAlchemy (ORM)
- PostgreSQL (Production database)
- HTML / CSS
- Jinja2 Templates
- Gunicorn (Deployment server)
- Render (Hosting platform)

---

## Database

- PostgreSQL used in production
- SQLite used only in local development (optional)

---

## Installation (Local Setup)

```bash
git clone https://github.com/your-username/helpdesk-system.git
cd helpdesk-system
pip install -r requirements.txt
python app.py
```
