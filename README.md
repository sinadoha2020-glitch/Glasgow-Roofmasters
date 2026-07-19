# Glasgow Roofmasters — Full-Stack Website

A complete, production-ready website for Glasgow Roofmasters built with Python Flask.

## Features

- **Backend**: Python Flask with SQLAlchemy ORM
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Forms**: AJAX submission with validation, loading/success/error states
- **Rate Limiting**: 5 requests/minute per IP
- **Email**: Flask-Mail for notifications
- **SEO**: Meta tags, Open Graph, LocalBusiness Schema.org JSON-LD
- **Accessibility**: WCAG AA contrast, skip links, ARIA labels
- **Responsive**: Mobile-first with sticky mobile bottom bar
- **Animations**: Scroll reveal, hover effects, prefers-reduced-motion support
- **CMS Fields**: All business details in centralised config
- **Admin Panel**: `/admin/requests` to view submissions

## Pages

1. Home
2. About Us
3. Services (with 5 sub-pages)
4. Pricing
5. Service Areas
6. Gallery
7. FAQ
8. Contact

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python run.py

# Or with Docker
docker-compose up --build
```

## Production

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app
```
