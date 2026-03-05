<div align="center">

# 📁 Minfin File Collector

**A production-ready Django REST API backend with JWT authentication, OTP email verification, async task processing, and full Swagger documentation — fully containerized with Docker.**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-Latest-red?style=flat-square)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7.2-DC382D?style=flat-square&logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![Celery](https://img.shields.io/badge/Celery-5.3-37814A?style=flat-square&logo=celery&logoColor=white)](https://docs.celeryproject.org/)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [API Reference](#-api-reference)
- [Authentication Flow](#-authentication-flow)
- [User Model](#-user-model)
- [Docker Services](#-docker-services)
- [Management Commands](#-management-commands)
- [Development Tips](#-development-tips)

---

## 🔍 Overview

Minfin File Collector is the backend API for a document/file collection system built for the **Ministry of Finance**. It provides:

- 🔐 Secure user registration with **OTP email verification**
- 🪙 **JWT-based authentication** (access + refresh tokens)
- 👤 Full **user profile management** with avatar support
- 📧 **Password reset** via OTP
- ⚙️ **Celery** task queue ready for background jobs
- 📖 **Swagger / ReDoc** auto-generated API docs
- 🐳 Fully **Dockerized** — one command to run everything

---

## 🧱 Tech Stack

| Layer | Technology | Version |
|---|---|---|
| **Language** | Python | 3.11 |
| **Framework** | Django + Django REST Framework | 5.2 |
| **Database** | PostgreSQL | 16 |
| **Cache / Message Broker** | Redis | 7.2 Alpine |
| **Task Queue** | Celery + django-celery-beat | 5.3 |
| **Authentication** | SimpleJWT | 5.3 |
| **API Documentation** | drf-yasg (Swagger + ReDoc) | 1.21 |
| **Web Server** | Gunicorn (12 workers) | latest |
| **Containerization** | Docker + Docker Compose | v3.8 |
| **Image Processing** | Pillow | 12.0 |

---

## 📂 Project Structure

```
minfin-file-collector/
│
├── core/                          # Project configuration
│   ├── settings.py                # Django settings (env-driven)
│   ├── urls.py                    # Root URL routing
│   ├── celery.py                  # Celery application
│   ├── schema.py                  # Swagger/ReDoc URL patterns
│   ├── views.py                   # Health check endpoint
│   ├── generator.py               # Custom ID / code generators
│   ├── jazzmin_conf.py            # Admin UI configuration
│   ├── asgi.py
│   └── wsgi.py
│
├── users/                         # Authentication & user management
│   ├── models.py                  # Custom User + OTPCode models
│   ├── views.py                   # Auth endpoints (register, login, OTP…)
│   ├── serializers.py             # Request/response serializers
│   ├── urls.py                    # User URL routes
│   ├── utils.py                   # OTP email sender
│   ├── admin.py
│   └── management/commands/
│       ├── create_demo_users.py   # Seed demo users
│       └── createsuperuser.py     # Custom superuser creation
│
├── common/                        # Shared abstractions
│   └── models.py                  # BaseModel (created/updated timestamps)
│
├── data/
│   └── region_districts.json      # Geographic fixture data
│
├── media/                         # User-uploaded files (gitignored)
├── static/                        # Collected static files (gitignored)
│
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh                  # migrate → collectstatic → gunicorn
├── requirements.txt
└── .env                           # Local environment variables
```

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) & Docker Compose
- Git

### 1 · Clone

```bash
git clone <repository-url>
cd minfin-file-collector
```

### 2 · Configure environment

```bash
cp .env.example .env   # then edit .env with your values
```

> See the [Environment Variables](#-environment-variables) section for all options.

### 3 · Fix entrypoint permissions (first time only)

```bash
chmod +x entrypoint.sh
```

### 4 · Build & run

```bash
docker compose up --build
```

The API will be live at **[http://localhost:8000](http://localhost:8000)**

### 5 · Seed demo users *(optional)*

```bash
docker compose exec web python manage.py create_demo_users
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
# ── Project ──────────────────────────────────────────────
PROJECT_NAME=django_base

# ── Django ───────────────────────────────────────────────
SECRET_KEY=change-me-in-production
DEBUG=1
DJANGO_SETTINGS_MODULE=core.settings
WEB_PORT=8000
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
CSRF_TRUSTED_ORIGINS=http://localhost:8000
IS_API_PROTECTED=0

# ── Database ─────────────────────────────────────────────
DB_ENGINE=django.db.backends.postgresql
DB_NAME=django_base
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# ── Celery / Redis ───────────────────────────────────────
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# ── Email ────────────────────────────────────────────────
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=no-reply@example.com
```

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | — | Django secret key — **change in production** |
| `DEBUG` | `1` | `0` for production |
| `WEB_PORT` | `8000` | Exposed container port |
| `IS_API_PROTECTED` | `0` | Global API protection toggle |
| `CORS_ALLOWED_ORIGINS` | localhost origins | Comma-separated frontend origins |
| `EMAIL_BACKEND` | console | Use SMTP backend for real emails |

---

## 🔌 API Reference

**Base URL:** `http://localhost:8000/api/`

### 🩺 System

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health/` | Health check |

### 👤 Users & Authentication

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/users/check-email/` | Check if an email is registered | ❌ |
| `POST` | `/api/users/register/` | Register a new user | ❌ |
| `POST` | `/api/users/verify-otp/` | Verify OTP code (registration / password reset) | ❌ |
| `POST` | `/api/users/resend-otp/` | Resend OTP to email | ❌ |
| `POST` | `/api/users/login/` | Login — returns access + refresh tokens | ❌ |
| `POST` | `/api/users/refresh/` | Refresh access token | ❌ |
| `POST` | `/api/users/password-reset/` | Request password reset OTP | ❌ |
| `POST` | `/api/users/password-reset-confirm/` | Set new password using OTP | ❌ |
| `GET / PATCH` | `/api/users/profile/` | View or update own profile | ✅ Bearer |
| `POST` | `/api/users/password-change/` | Change password (authenticated) | ✅ Bearer |

### 📚 API Documentation

| Interface | URL |
|---|---|
| **Swagger UI** | [http://localhost:8000/swagger/](http://localhost:8000/swagger/) |
| **ReDoc** | [http://localhost:8000/redoc/](http://localhost:8000/redoc/) |
| **Admin Panel** | [http://localhost:8000/api/admin/](http://localhost:8000/api/admin/) |

---

## 🔐 Authentication Flow

```
┌─────────┐     POST /register      ┌─────────────┐
│  Client │ ──────────────────────► │   Backend   │
└─────────┘                         └──────┬──────┘
                                           │ sends OTP email
                                           ▼
                                    ┌─────────────┐
                                    │  OTP Code   │  (6 digits, 10 min expiry)
                                    └──────┬──────┘
                                           │
┌─────────┐    POST /verify-otp     ┌──────▼──────┐
│  Client │ ──────────────────────► │   Backend   │
└─────────┘                         └──────┬──────┘
                                           │ email verified ✅
                                           ▼
                                  ┌─────────────────────┐
                                  │  JWT Tokens issued  │
                                  │  Access  (1 hour)   │
                                  │  Refresh (7 days)   │
                                  └─────────────────────┘

Password Reset follows the same OTP flow:
  POST /password-reset  →  OTP email  →  POST /password-reset-confirm
```

**Token usage:**
```http
Authorization: Bearer <access_token>
```

---

## 👤 User Model

The custom `User` model extends Django's `AbstractUser`:

| Field | Type | Description |
|---|---|---|
| `username` | CharField | Unique username |
| `email` | EmailField | Unique email address |
| `full_name` | CharField | Display name |
| `phone_number` | CharField | Contact phone |
| `avatar` | ImageField | Profile picture (`user_avatars/`) |
| `language` | CharField | UI language: `en` · `uz` · `ru` |
| `email_verified` | BooleanField | Whether OTP was confirmed |
| `is_staff` | BooleanField | Django admin access |
| `is_superuser` | BooleanField | Full permissions |

---

## 🐳 Docker Services

| Service | Container | Image | Port |
|---|---|---|---|
| **web** | `${PROJECT_NAME}_backend` | Custom build | `8000` |
| **db** | `${PROJECT_NAME}_db` | `postgres:16` | internal `5432` |
| **redis** | `${PROJECT_NAME}_redis` | `redis:7.2.4-alpine` | internal `6379` |

> **Celery worker** and **Celery Beat** are defined in `docker-compose.yml` and can be enabled by uncommenting those service blocks.

### Startup sequence (`entrypoint.sh`)

```
python manage.py migrate
  └─► python manage.py collectstatic --noinput
        └─► gunicorn core.wsgi:application --bind 0.0.0.0:$WEB_PORT --workers=12
```

---

## 🛠️ Management Commands

### `create_demo_users`

Seeds an admin and a test user for local development:

```bash
# Create demo users (skips if already exist)
docker compose exec web python manage.py create_demo_users

# Custom credentials
docker compose exec web python manage.py create_demo_users \
  --admin-email admin@myapp.com \
  --admin-password SuperSecret123 \
  --user-email dev@myapp.com \
  --user-password DevPass123
```

| Account | Email | Password | Role |
|---|---|---|---|
| Admin | `admin@example.com` | `admin123` | Superuser |
| User | `test@example.com` | `testpass123` | Regular |

### Other useful commands

```bash
# Apply database migrations
docker compose exec web python manage.py migrate

# Open Django shell
docker compose exec web python manage.py shell

# Create a superuser interactively
docker compose exec web python manage.py createsuperuser

# Seed demo users (admin + test user)
docker compose exec web python manage.py create_demo_users

# Seed demo users with custom credentials
docker compose exec web python manage.py create_demo_users \
  --admin-email admin@myapp.com \
  --admin-password SuperSecret123 \
  --user-email dev@myapp.com \
  --user-password DevPass123

# Collect static files
docker compose exec web python manage.py collectstatic --noinput
```

---

## 💡 Development Tips

```bash
# Start everything
docker compose up --build

# Run in background
docker compose up -d

# Tail logs
docker compose logs -f web

# Stop & remove containers
docker compose down

# Stop & remove containers + volumes (⚠️ wipes DB)
docker compose down -v

# Rebuild only the web image
docker compose build web
```

**Enable Celery** — uncomment the `celery` and `celery-beat` blocks in `docker-compose.yml`, then:

```bash
docker compose up --build
```

---

<div align="center">

Built with ❤️ for the **Ministry of Finance** · Powered by Django & Docker

</div>
