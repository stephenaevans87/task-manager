# Flask Task Manager

A full-stack task management application built with **Flask**, **React**, and **PostgreSQL**.

This project was developed from scratch as a learning project focused on modern web development practices. It evolved over multiple development sessions from a simple Flask application into a production-ready full-stack application featuring authentication, REST APIs, database persistence, cloud deployment, and a React frontend.

---

# Features

## User Management

- User registration
- Secure login/logout
- Password hashing
- Session authentication
- User-specific task ownership

## Task Management

- Create tasks
- Edit tasks
- Delete tasks
- Mark tasks complete/incomplete
- Search tasks
- Filter tasks
- Sort tasks
- Priority levels
- Categories
- Due dates
- Overdue detection

## Backend

- Flask
- SQLAlchemy ORM
- Flask-Migrate
- REST API
- SQLite (development)
- PostgreSQL (production)

## Frontend

- React
- Vite
- Responsive design

## Deployment

- Git
- GitHub
- Render
- Gunicorn
- Continuous Deployment (CI/CD)

---

# Technology Stack

## Backend

- Python
- Flask
- SQLAlchemy
- Flask-Migrate
- Gunicorn

## Frontend

- React
- Vite
- JavaScript
- HTML
- CSS

## Database

- SQLite (local development)
- PostgreSQL (production)

## Deployment

- Render
- GitHub

---

# Screenshots

*(Screenshots will be added here.)*

Suggested screenshots:

- Login page
- Registration page
- Task dashboard
- Edit task page
- Mobile responsive view

---

# Local Installation

Clone the repository:

```bash
git clone https://github.com/YOstephenaevans87/task-manager.git
```

Enter the project:

```bash
cd task-manager
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install frontend dependencies:

```bash
cd frontend
npm install
```

---

# Running the Application

## Terminal 1 — Flask Backend

```bash
cd ~/task-manager
source venv/bin/activate
python app.py
```

The Flask API runs at:

```
http://127.0.0.1:5000
```

---

## Terminal 2 — React Frontend

```bash
cd ~/task-manager/frontend
npm run dev
```

Open the Vite URL displayed in the terminal (typically):

```
http://localhost:5173
```

---

# Database Migrations

Create a migration:

```bash
flask db migrate -m "Description"
```

Apply migrations:

```bash
flask db upgrade
```

---

# Production Deployment

The application is deployed on **Render**.

Deployment is fully automated through GitHub.

Every push to the main branch automatically triggers a new deployment.

Production start command:

```bash
flask db upgrade && gunicorn app:app
```

---

# Project Structure

```
task-manager/
│
├── frontend/
│   ├── public/
│   └── src/
│
├── instance/
│
├── migrations/
│
├── routes/
│
├── static/
│
├── templates/
│
├── app.py
├── config.py
├── models.py
├── storage.py
├── utils.py
├── requirements.txt
└── README.md
```

---

## Environment Variables

Create a `.env` file in the project root.

Example:

```text
FLASK_ENV=development
SECRET_KEY=your-random-secret-key
DATABASE_URL=sqlite:///tasks.db
```

For production (Render), configure these variables in the Render dashboard rather than committing them to Git.

## Security Features

This project includes several security best practices appropriate for a portfolio-quality Flask application:

- Password hashing using Werkzeug
- Session-based authentication
- User-specific authorization checks
- Email verification with signed, expiring tokens
- Rate limiting with Flask-Limiter
- Secure handling of environment variables and secrets
- SQLAlchemy ORM to prevent SQL injection
- Automatic HTML escaping through Jinja2 templates
- Server-side input validation
- Secure session cookie configuration
- Generic error responses that avoid exposing sensitive information

### Known Limitations

This project intentionally omits several advanced production features in order to remain educational and approachable:

- Password reset
- Multi-factor authentication (MFA)
- OAuth / Social login
- CSRF protection
- Content Security Policy (CSP)
- Advanced audit logging

# Future Improvements

Possible future enhancements include:

- Email reminders
- Push notifications
- Background task scheduling
- Docker support
- Automated testing
- OAuth authentication
- Calendar integration
- Mobile application

---

# Lessons Learned

This project provided practical experience with:

- Flask application architecture
- REST API development
- SQLAlchemy ORM
- Database migrations
- Authentication and authorization
- React frontend development
- Cloud deployment
- CI/CD workflows
- PostgreSQL
- Git and GitHub collaboration
- Full-stack application design

---

# License

This project is licensed under the MIT License.