# 🚀 Rush Republic - Employee Management & Authentication Portal

A full-stack enterprise authentication and role-based department portal built for **Rush Republic**, powered by **Django REST Framework (DRF)** on the backend and **React** on the frontend with **JWT authentication**, **PostgreSQL database**, and strict **Role-Based Access Control (RBAC)**.

---

## 📌 Table of Contents

- [Overview & Features](#-overview--features)
- [Architecture & Tech Stack](#-architecture--tech-stack)
- [Project Directory Structure](#-project-directory-structure)
- [Prerequisites](#-prerequisites)
- [Step-by-Step Setup & Run Commands](#-step-by-step-setup--run-commands)
  - [1. Database Setup (PostgreSQL)](#1-database-setup-postgresql)
  - [2. Backend Setup (Django & DRF)](#2-backend-setup-django--drf)
  - [3. Frontend Setup (React.js)](#3-frontend-setup-reactjs)
- [Quick Reference: All Commands](#-quick-reference-all-commands)
- [Environment Variables (.env) Reference](#-environment-variables-env-reference)
- [API Endpoints Reference](#-api-endpoints-reference)
- [User Roles & Dashboard Routing](#-user-roles--dashboard-routing)
- [Troubleshooting & FAQs](#-troubleshooting--faqs)

---

## ✨ Overview & Features

- **Custom User Model**: Uses `email` as the unique login credential alongside `username`, `contact`, and `department`.
- **JWT Authentication**: Secure access & refresh tokens via SimpleJWT with automatic token rotation and blacklisting on logout.
- **Department Role-Based Routing**: Dynamic navigation and permissions based on employee department:
  - 👑 **Admin** (`ADMIN`): Full access to admin overview, analytics, user roster, and department homepages.
  - 📱 **Social Media** (`SOCIAL_MEDIA`): Dedicated dashboard for Social Media team.
  - 🎬 **Production Co-Ordinator** (`PRODUCTION_COORDINATOR`): Tailored workflow dashboard.
  - 🤝 **Client-Servicing** (`CLIENT_SERVICING`): Client-facing management interface.
- **Secure Password Policy**: Client and server-side validation enforcing min 8 characters, uppercase, lowercase, number, and special character.
- **Modern React Interface**: Clean, responsive UI with route protection guards (`ProtectedRoute`, `RoleProtectedRoute`), Axios interceptors with silent token refresh, and custom typography.

---

## 🛠 Architecture & Tech Stack

### **Backend**
- **Framework**: Django 5.0.6 & Django REST Framework (DRF) 3.15.1
- **Authentication**: `djangorestframework-simplejwt` 5.3.1 (JSON Web Tokens)
- **Database**: PostgreSQL with `psycopg2-binary` 2.9.9
- **CORS Handling**: `django-cors-headers` 4.3.1
- **Configuration**: `python-decouple` 3.8

### **Frontend**
- **Framework**: React 18.3.1
- **Routing**: React Router DOM v6 (`react-router-dom` 6.24.0)
- **HTTP Client**: Axios 1.19.0 (with request/response interceptors for JWT token auto-refresh)
- **Typography & Styling**: Mona Sans & Manrope Google fonts, custom vanilla CSS design system

---

## 📁 Project Directory Structure

```text
rush-republic/
├── backend/
│   ├── manage.py                     # Django management script
│   ├── requirements.txt              # Python dependencies
│   ├── .env                          # Backend environment variables
│   ├── rush_republic/                # Django project settings
│   │   ├── __init__.py
│   │   ├── settings.py               # Main configuration (DB, JWT, CORS, Apps)
│   │   ├── urls.py                   # Root URL routing
│   │   ├── asgi.py
│   │   └── wsgi.py
│   └── users/                        # Users & Authentication app
│       ├── models.py                 # CustomUser & Department choices
│       ├── serializers.py            # Signup, Login, and User serializers
│       ├── views.py                  # Signup, Login, Logout, and Department views
│       ├── permissions.py            # RBAC custom permissions
│       ├── urls.py                   # API routes
│       └── admin.py                  # Django Admin registrations
│
└── frontend/
    ├── package.json                  # Node.js dependencies and scripts
    ├── .env                          # Frontend environment variables
    ├── .env.example
    ├── public/
    │   └── index.html
    └── src/
        ├── App.js                    # React router & role protection routes
        ├── index.js                  # Entry point
        ├── index.css                 # Global theme & typography
        ├── api/
        │   └── axios.js              # Axios instance with JWT interceptors
        ├── context/
        │   └── AuthContext.js        # Global authentication state provider
        ├── components/
        │   ├── ProtectedRoute.js     # Auth verification guard
        │   └── RoleProtectedRoute.js # Role-based access guard
        └── pages/
            ├── Login.js              # Login page
            ├── Signup.js             # Registration with validation
            ├── AdminHome.js          # Admin dashboard & stats
            ├── SocialMediaHome.js    # Social Media home
            ├── ProductionCoordinatorHome.js # Production coordinator home
            ├── ClientServicingHome.js# Client servicing home
            ├── Unauthorized.js       # 403 Forbidden page
            ├── Auth.css              # Authentication pages styling
            └── Home.css              # Dashboard pages styling
```

---

## 📋 Prerequisites

Before running the project, make sure you have the following installed on your machine:

1. **Python** (version 3.10 or higher) - [Download Python](https://www.python.org/downloads/)
2. **Node.js** (v18.x or v20.x LTS) & **npm** - [Download Node.js](https://nodejs.org/)
3. **PostgreSQL** Server (v14, v15, or v16) - [Download PostgreSQL](https://www.postgresql.org/download/)
4. **Git** - [Download Git](https://git-scm.com/)

---

## ⚙️ Step-by-Step Setup & Run Commands

### 1. Database Setup (PostgreSQL)

Open PostgreSQL terminal (`psql`) or **pgAdmin** and run the following SQL commands to create the database and user:

```sql
-- Create database
CREATE DATABASE rush_republic_db;

-- Create user with password
CREATE USER rush_republic_user WITH PASSWORD 'change-this-password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE rush_republic_db TO rush_republic_user;

-- Connect to database and grant schema privileges (required on PostgreSQL 15+)
\c rush_republic_db
GRANT ALL ON SCHEMA public TO rush_republic_user;
```

---

### 2. Backend Setup (Django & DRF)

#### Step 2.1: Open a terminal and navigate to the backend directory
```bash
cd rush-republic/backend
```

#### Step 2.2: Create and activate a Python virtual environment

- **On Windows (PowerShell / Command Prompt):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```

- **On macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

#### Step 2.3: Install backend dependencies
```bash
pip install -r requirements.txt
```

#### Step 2.4: Configure Backend Environment Variables
Create or verify the `.env` file inside `rush-republic/backend/.env`:

```env
SECRET_KEY=django-insecure-your-custom-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=rush_republic_db
DB_USER=rush_republic_user
DB_PASSWORD=change-this-password
DB_HOST=127.0.0.1
DB_PORT=5432
CORS_ORIGIN=http://localhost:3000
```

#### Step 2.5: Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Step 2.6: Create a Superuser / Admin Account
```bash
python manage.py createsuperuser
```
*(Enter username, email, contact number, department as `ADMIN`, and password when prompted)*

#### Step 2.7: Start the Django Development Server
```bash
python manage.py runserver 8000
```
> 🌐 Backend API is now running at: **`http://127.0.0.1:8000/`**  
> 🛡️ Django Admin Portal is at: **`http://127.0.0.1:8000/admin/`**

---

### 3. Frontend Setup (React.js)

#### Step 3.1: Open a NEW terminal and navigate to the frontend directory
```bash
cd rush-republic/frontend
```

#### Step 3.2: Install Node.js dependencies
```bash
npm install
```

#### Step 3.3: Configure Frontend Environment Variables
Create or verify the `.env` file inside `rush-republic/frontend/.env`:

```env
REACT_APP_API_BASE_URL=http://localhost:8000/api
```

#### Step 3.4: Start the React Development Server
```bash
npm start
```
> 🚀 Frontend Application will open automatically at: **`http://localhost:3000/`**

---

## ⚡ Quick Reference: All Commands

### 🖥️ Backend Terminal (Terminal 1)
```powershell
# 1. Navigate to backend
cd rush-republic/backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment (Windows)
.\venv\Scripts\activate
# (macOS/Linux: source venv/bin/activate)

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run database migrations
python manage.py makemigrations
python manage.py migrate

# 6. (Optional) Create Admin Superuser
python manage.py createsuperuser

# 7. Start backend server
python manage.py runserver 8000
```

### 💻 Frontend Terminal (Terminal 2)
```powershell
# 1. Navigate to frontend
cd rush-republic/frontend

# 2. Install dependencies
npm install

# 3. Start frontend server
npm start
```

---

## 🔑 Environment Variables (.env) Reference

### Backend (`rush-republic/backend/.env`)

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `SECRET_KEY` | `j2v3p_n...` | Django cryptographic secret key |
| `DEBUG` | `True` | Debug mode (`True` for local development, `False` for production) |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated allowed hostnames |
| `DB_NAME` | `rush_republic_db` | PostgreSQL database name |
| `DB_USER` | `rush_republic_user` | PostgreSQL database username |
| `DB_PASSWORD` | `change-this-password` | PostgreSQL database password |
| `DB_HOST` | `127.0.0.1` | Database host |
| `DB_PORT` | `5432` | Database port |
| `CORS_ORIGIN` | `http://localhost:3000` | Allowed React frontend origins |

### Frontend (`rush-republic/frontend/.env`)

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `REACT_APP_API_BASE_URL` | `http://localhost:8000/api` | Base URL for Django REST backend API |

---

## 🌐 API Endpoints Reference

All API routes are prefixed with `/api/`:

| Method | Endpoint | Access Level | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/signup/` | Public | Register new employee account |
| `POST` | `/api/login/` | Public | Authenticate email + password, returns JWT tokens & user profile |
| `POST` | `/api/login/refresh/` | Public | Obtain new access token using refresh token |
| `POST` | `/api/logout/` | Authenticated | Blacklist refresh token and log out |
| `GET` | `/api/profile/` | Authenticated | Retrieve current authenticated user profile |
| `GET` | `/api/admin-dashboard/` | `ADMIN` | Admin metrics, department stats, and user list |
| `GET` | `/api/social-media/` | `SOCIAL_MEDIA` / `ADMIN` | Social Media department landing data |
| `GET` | `/api/production-coordinator/` | `PRODUCTION_COORDINATOR` / `ADMIN` | Production Co-Ordinator landing data |
| `GET` | `/api/client-servicing/` | `CLIENT_SERVICING` / `ADMIN` | Client-Servicing landing data |
| `ALL` | `/admin/` | Staff/Superuser | Built-in Django Admin Interface |

---

## 🛡️ User Roles & Dashboard Routing

Employees are redirected automatically to their designated dashboard after signing in:

| Department Code | Department Name | Allowed Route |
| :--- | :--- | :--- |
| `ADMIN` | Admin | `/admin-home` (also has access to all dashboards) |
| `SOCIAL_MEDIA` | Social Media | `/social-media-home` |
| `PRODUCTION_COORDINATOR` | Production Co-Ordinator | `/production-coordinator-home` |
| `CLIENT_SERVICING` | Client-Servicing | `/client-servicing-home` |

- **Unauthorized Access**: If a user attempts to access a page outside their department permission, they are safely redirected to `/unauthorized`.

---

## ❓ Troubleshooting & FAQs

### 1. Database connection failed (`OperationalError: could not connect to server`)
- Ensure PostgreSQL service is running on your machine:
  - Windows: Check `services.msc` -> ensure **postgresql-x64** is running.
  - Linux: `sudo systemctl status postgresql`
  - macOS: `brew services list`
- Double-check that `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT` in `backend/.env` match your PostgreSQL setup.

### 2. CORS Errors in Browser Console
- Verify that `CORS_ORIGIN=http://localhost:3000` is present in `backend/.env`.
- Ensure backend server was restarted after changing `.env`.

### 3. Port Conflicts (Port 8000 or 3000 already in use)
- **Django**: Run on another port:
  ```bash
  python manage.py runserver 8080
  ```
  *(Remember to update `REACT_APP_API_BASE_URL=http://localhost:8080/api` in `frontend/.env`)*
- **React**: React will prompt you automatically to use another port (e.g., port 3001) if 3000 is occupied.

### 4. JWT Token Expiration
- Access tokens expire every 60 minutes and refresh tokens rotate every 7 days.
- The frontend Axios interceptor automatically handles refreshing the token in the background.

---

## 👥 Contributors & License

- **Project**: Rush Republic Employee Management Portal
- **Maintained for**: Rush Republic Internal Operations
