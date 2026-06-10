<div align="center">

# 🚀 StartKH

**Cambodia's Startup & Project Discovery Platform**

*Discover, collaborate, and build the next generation of Cambodian tech projects.*

[![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-MariaDB-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com)

</div>

---

## 📖 About

**StartKH** is a community-driven discovery platform for Cambodian startups and tech projects. Makers can showcase their work, get upvotes from the community, recruit team members, and track project analytics — all in one place.

Think of it as **Product Hunt**, but built specifically for Cambodia's growing tech ecosystem.

---

## ✨ Features

- 🔍 **Project Discovery** — Explore and search projects by category, trending score, or newest
- 👤 **User Profiles** — Customizable profiles with skills, social links (GitHub, Telegram, Facebook, LinkedIn)
- 📦 **Project Submission** — Submit projects with logo, cover image, tagline, description, website, GitHub, and video demo
- 👍 **Voting System** — Upvote projects to boost their trending score
- 💬 **Comments** — Community discussions on each project page
- 🔥 **Trending Algorithm** — Score = `(Upvotes × 15) + (Comments × 5) + Views`
- 👥 **Team Recruitment** — Post open positions and accept applications from the community
- 🔔 **Notifications** — Real-time in-app notifications for key activity
- 📊 **Analytics Dashboard** — View counts and engagement insights per project
- 🔎 **Global Search** — Search across projects and users
- 🗂️ **Categories** — Browse projects by tech category
- 📧 **Password Reset** — Full email-based password recovery flow

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django (Python) |
| Database | MySQL / MariaDB (with SQLite fallback) |
| Frontend | Bootstrap 5, Crispy Forms |
| API | Django REST Framework |
| Timezone | Asia/Phnom_Penh (UTC+7) |
| Media | Pillow (image uploads) |

---

## 📁 Project Structure

```
StartKH/
├── apps/
│   ├── accounts/        # User registration, login, profiles
│   ├── analytics/       # Project view & engagement tracking
│   ├── categories/      # Project categories
│   ├── comments/        # Project comment system
│   ├── core/            # Shared utilities and base views
│   ├── dashboard/       # User dashboard
│   ├── notifications/   # In-app notification system
│   ├── projects/        # Project CRUD, listing, detail
│   ├── search/          # Global search functionality
│   ├── teams/           # Team positions & applications
│   └── votes/           # Upvote system
├── config/
│   ├── settings.py      # Django settings
│   ├── urls.py          # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── static/
│   ├── css/custom.css   # Custom styles
│   └── images/          # Default images & OG image
├── templates/           # HTML templates (per app)
├── media/               # User-uploaded files (gitignored)
└── manage.py
```

---

## ⚙️ Local Development Setup

### Prerequisites

- Python 3.10+
- XAMPP (for MySQL/MariaDB) **or** just use the SQLite fallback
- Git

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/StartKH.git
cd StartKH
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install django mysqlclient pillow django-crispy-forms crispy-bootstrap5 djangorestframework
```

### 4. Configure the database

**Option A — MySQL (recommended):**
Start XAMPP and make sure Apache & MySQL are running. The app will auto-create the `startkh` database on first run.

**Option B — SQLite (no setup needed):**
If MySQL is not available, the app automatically falls back to SQLite.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** in your browser. 🎉

---

## 🔑 Environment Variables

> ⚠️ For production, move sensitive values to a `.env` file and use `python-decouple` or `django-environ`.

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key | Set in `settings.py` |
| `DEBUG` | Debug mode | `True` |
| `DB_NAME` | MySQL database name | `startkh` |
| `DB_USER` | MySQL username | `root` |
| `DB_PASSWORD` | MySQL password | *(empty)* |
| `DB_HOST` | MySQL host | `127.0.0.1` |
| `DB_PORT` | MySQL port | `3306` |

---

## 🧩 App Overview

### `accounts`
Handles user registration, login/logout, profile management, and password reset. Each user automatically gets a `Profile` (created via Django signals) with avatar, bio, skills, and social links.

### `projects`
Core app. Projects have a title, slug, logo, cover image, tagline, description, website, GitHub, video demo link, and a moderation status (`pending` / `approved` / `rejected`).

### `votes`
Simple upvote system. Each user can vote once per project. Vote count feeds into the trending score.

### `comments`
Comment threads on project pages.

### `teams`
Project owners can post `TeamPosition` openings (e.g. "Developer", "Designer"). Users submit `Application` objects with a cover message.

### `notifications`
In-app notifications delivered via a custom context processor so the notification count is available across all templates.

### `analytics`
Tracks project view counts and engagement for the analytics dashboard.

### `search`
Full text search across projects and user profiles.

### `categories`
Taxonomy for filtering projects by tech category.

### `dashboard`
Personalized user homepage showing their projects, applications, and activity.

---

## 🚀 Deployment (Production Checklist)

- [ ] Set `DEBUG = False`
- [ ] Set a strong, random `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Switch `EMAIL_BACKEND` to SMTP (e.g. Gmail, SendGrid)
- [ ] Run `python manage.py collectstatic`
- [ ] Serve media files via Nginx or a CDN
- [ ] Use environment variables for all secrets

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

Built with ❤️ for Cambodia's tech community 🇰🇭

</div>
