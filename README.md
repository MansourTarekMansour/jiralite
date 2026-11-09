# ⚡ JiraLite

> **JiraLite** is a streamlined Jira & Agile Kanban task tracker built with **Django 4.2+** using a clean, enterprise modular architecture tailored for **Laravel & Backend Engineers**.

---

## 🏗️ Project Architecture

```text
jiralite/
├── manage.py                     # Laravel: artisan
├── config/                       # Laravel: config/ + bootstrap/
│   ├── settings.py               # Kernel config, middleware, databases, installed apps
│   ├── urls.py                   # Root URL router (Laravel: routes/web.php)
│   ├── wsgi.py                   # HTTP web server entrypoint
│   └── asgi.py                   # Async / WebSocket entrypoint (Laravel Octane/Reverb)
│
├── tracker/                      # Domain Feature Module (Laravel: app/)
│   ├── models/                   # Eloquent models (Project, Issue, ProjectMember)
│   ├── views/                    # Controllers (ProjectController, IssueController)
│   ├── forms/                    # Request Validation & DTOs (FormRequest equivalent)
│   ├── middleware.py             # Custom HTTP middlewares (Tenant / Timing)
│   ├── permissions.py            # Custom Policies & Gates
│   └── urls.py                   # Domain routing (routes/tracker.php)
│
├── templates/                    # Laravel: resources/views/ (Blade templates)
│   ├── base.html                 # App layout (@extends)
│   ├── components/               # Blade components (Navbar, Alerts, Modals)
│   └── tracker/                  # Feature views (Board, Details, Project list)
│
├── docs/                         # Architecture Documentation
│   └── erd/                      # Interactive Entity Relationship Diagrams
│       └── jiralite-erd.html
└── static/                       # Compiled assets (CSS / JS)
```

---

## 🗺️ Laravel ➔ Django Rosetta Stone

| Laravel Concept | Django Equivalent | Notes |
| :--- | :--- | :--- |
| `php artisan` | `python manage.py` | Command line runner |
| `composer.json` | `requirements.txt` / `pip` | Package manager |
| `vendor/` | `.venv/` | Isolated runtime & packages |
| **Eloquent Model** | **Django Declarative Model** | Declared in `tracker/models/` |
| **Controller** | **Views** (`tracker/views/`) | Django calls controllers "Views" |
| **Blade** (`.blade.php`) | **Django Template Language (DTL)** | Located in `templates/` |
| **FormRequest** | **ModelForm / Forms** | Validates input & binds HTML forms |
| **Route Middleware** | **Django Middleware** | Callable class with `get_response` |
| **Policies / Gates** | **Django Permissions & Mixins** | Defined in `tracker/permissions.py` |
| **Laravel Nova / Filament** | **Django Admin** (`/admin/`) | Built-in free admin CRUD panel |

---

## 📊 Database Schema & ERD

The interactive visual Entity Relationship Diagram is available at:
👉 **[`docs/erd/jiralite-erd.html`](docs/erd/jiralite-erd.html)**

### Core Tables:
1. **`projects`**: Workspace container (`name`, `key` like `JIRA`, `lead_id`, cached counters).
2. **`project_members`**: RBAC Pivot model (`ADMIN`, `DEVELOPER`, `VIEWER`).
3. **`issues`**: Kanban tasks (`BUG`, `TASK`, `STORY`) with states (`TODO`, `IN_PROGRESS`, `DONE`).
4. **`issue_activity_logs`**: Immutable audit log of status transitions and assignments.
5. **`users`**: Django core `auth_user`.

---

## 🚀 Quick Start Guide

### 1. Activate Environment
```bash
source .venv/bin/activate
```

### 2. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 4. Start Development Server
```bash
python manage.py runserver
```

Open:
* **Web Application:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **Django Admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)