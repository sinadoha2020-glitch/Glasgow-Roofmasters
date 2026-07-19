# Glasgow Roofmasters — Professional Roofing Website

[![Render](https://img.shields.io/badge/Render-Deployed-blue?logo=render)](https://glasgowroofmasters.co.uk)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> A complete, production-ready full-stack website for Glasgow Roofmasters — a professional roofing company based in Glasgow, Scotland.

## 🚀 Live Demo

**Production**: [https://glasgowroofmasters.co.uk](https://glasgowroofmasters.co.uk)  
**Staging**: [https://glasgow-roofmasters-staging.onrender.com](https://glasgow-roofmasters-staging.onrender.com)

## 📸 Screenshots

| Home | Services | Contact |
|------|----------|---------|
| [Homepage](app/static/images/screenshots/home.png) | [Services](app/static/images/screenshots/services.png) | [Contact](app/static/images/screenshots/contact.png) |

## ✨ Features

- **8 Complete Pages**: Home, About, Services (×5), Pricing, Service Areas, Gallery, FAQ, Contact
- **Full-Stack Backend**: Python Flask with SQLAlchemy ORM
- **Database**: SQLite (development) / PostgreSQL (production)
- **Form Handling**: AJAX submission with validation, loading/success/error states
- **Rate Limiting**: Flask-Limiter (5 requests/minute per IP)
- **Email Notifications**: Flask-Mail for form submissions
- **SEO Optimized**: Schema.org JSON-LD, Open Graph, meta tags, sitemap.xml
- **Accessibility**: WCAG AA compliant, skip links, ARIA labels, `prefers-reduced-motion`
- **Responsive Design**: Mobile-first with sticky mobile bottom bar
- **CMS-Style Config**: All business details centralised for easy updates
- **Admin Panel**: `/admin/requests` to view inspection submissions

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, Flask 3.0 |
| Database | SQLAlchemy ORM, Flask-Migrate |
| Frontend | HTML5, CSS3, Vanilla JS (no frameworks) |
| Fonts | Barlow Condensed, Source Sans 3 (Google Fonts) |
| Hosting | Render (Cloud) |
| CI/CD | GitHub Actions |
| SSL | Auto-managed by Render |

## 🏁 Quick Start

### Prerequisites
- Python 3.11+
- pip
- Git

### Local Development

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/glasgow-roofmasters.git
cd glasgow-roofmasters

# 2. Create virtual environment
python -m venv venv

# 3. Activate (macOS/Linux)
source venv/bin/activate
# Activate (Windows)
# venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Environment variables
cp .env .env.local
# Edit .env.local with your settings

# 6. Initialize database
python -c "from app import app; from app import db; db.create_all()"

# 7. Run development server
python run.py

# 8. Open browser
open http://localhost:5000
```

### Docker

```bash
docker-compose up --build
```

## 📁 Project Structure

```
glasgow-roofmasters/
├── app.py                      # Main Flask application
├── config.py                   # Configuration classes
├── run.py                      # Development runner
├── wsgi.py                     # Production WSGI entry
├── requirements.txt            # Python dependencies
├── render.yaml               # Render Blueprint config
├── render-start.sh           # Render start script
├── Dockerfile                # Container config
├── docker-compose.yml        # Docker orchestration
├── .github/
│   └── workflows/
│       └── ci-cd.yml         # GitHub Actions pipeline
├── nginx/
│   └── glasgow-roofmasters.conf  # Nginx config
├── app/
│   ├── static/
│   │   ├── css/main.css      # Complete stylesheet
│   │   ├── js/main.js        # All frontend logic
│   │   ├── images/           # Assets
│   │   ├── robots.txt        # SEO robots
│   │   └── sitemap.xml       # SEO sitemap
│   └── templates/
│       ├── base.html         # Base template
│       ├── partials/         # Reusable components
│       ├── pages/            # 8 page templates
│       └── admin/            # Admin dashboard
└── tests/                    # Test suite
```

## 🌐 Pages

| Page | Route | Description |
|------|-------|-------------|
| Home | `/` | Hero, services, trust bar, gallery preview, FAQ, CTA |
| About | `/about` | Company story, credentials, [EDIT] placeholders |
| Services | `/services` | Overview of all 5 services |
| Service Detail | `/services/<slug>` | Individual service pages |
| Pricing | `/pricing` | Transparent pricing structure |
| Service Areas | `/service-areas` | Glasgow coverage map + 14 areas |
| Gallery | `/gallery` | Filterable masonry gallery |
| FAQ | `/faq` | 12 questions across 4 categories |
| Contact | `/contact` | Form, map, contact details |
| Admin | `/admin/requests` | View inspection submissions |

## 🔧 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | ✅ | Flask secret key |
| `DATABASE_URL` | ✅ | Database connection string |
| `MAIL_SERVER` | ❌ | SMTP server (default: smtp.gmail.com) |
| `MAIL_PORT` | ❌ | SMTP port (default: 587) |
| `MAIL_USERNAME` | ❌ | SMTP username |
| `MAIL_PASSWORD` | ❌ | SMTP password/app password |
| `MAIL_DEFAULT_SENDER` | ❌ | From address |

See [DEPLOYMENT.md](DEPLOYMENT.md) for full configuration.

## 🚀 Deployment

### Render (Recommended)

**One-Click Deploy:**
1. Fork this repo
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. New → Blueprint → Select this repo
4. Render auto-detects `render.yaml` and deploys everything

**Manual:**
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### GitHub + CI/CD

Every push to `main` automatically:
1. Runs tests
2. Lints code
3. Deploys to Render

Setup:
1. Add `RENDER_API_KEY` and `RENDER_SERVICE_ID` to GitHub Secrets
2. Push to `main`
3. Watch it deploy automatically

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Lint code
flake8 app.py config.py
black --check app.py config.py
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'feat: add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

## 📞 Support

For support, email post@glasgowroofmasters.co.uk or call 0141 266 0600.

---

<p align="center">
  <strong>Glasgow Roofmasters</strong> — Professional Roofing Services Across Glasgow
  <br>
  236 Sauchiehall St, Glasgow G2 3HQ | 0141 266 0600
</p>
