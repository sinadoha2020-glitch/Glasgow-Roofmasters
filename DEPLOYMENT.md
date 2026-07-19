# Deployment Guide

## Table of Contents
- [Render (Recommended)](#render-cloud-hosting)
- [GitHub + CI/CD](#github--cicd)
- [Manual Server](#manual-server-deployment)
- [Docker](#docker-deployment)
- [Domain & SSL](#custom-domain--ssl)
- [Environment Variables](#environment-variables-reference)

---

## Render Cloud Hosting (Recommended)

### Option A: Blueprint Deploy (One-Click)

1. Fork this repository to your GitHub account
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click **New +** → **Blueprint**
4. Connect your GitHub account and select this repo
5. Render will auto-detect `render.yaml` and create:
   - Web Service (Python)
   - PostgreSQL Database
   - Environment variables
6. Click **Apply** — deployment starts automatically

### Option B: Manual Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** → **Web Service**
3. Connect your GitHub repo
4. Configure:
   - **Name**: `glasgow-roofmasters`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 4 wsgi:app`
   - **Plan**: Starter ($7/month) or Free (sleeping)
5. Add Environment Variables (see below)
6. Click **Create Web Service**

### Option C: Deploy via CLI

```bash
# Install Render CLI
npm install -g @render/cli

# Login
render login

# Deploy from project root
render blueprint apply
```

---

## GitHub + CI/CD

### Repository Setup

1. Create a new repository on GitHub
2. Push this code:

```bash
git init
git add .
git commit -m "feat: initial full-stack website"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/glasgow-roofmasters.git
git push -u origin main
```

### GitHub Secrets (for auto-deploy)

Go to **Settings** → **Secrets and variables** → **Actions**:

| Secret Name | Value | How to Get |
|-------------|-------|------------|
| `RENDER_API_KEY` | `rnd_xxxxxxxx` | Render Dashboard → Account Settings → API Keys |
| `RENDER_SERVICE_ID` | `srv-xxxxxxxx` | Render Dashboard → Service → Settings → Copy ID |

Once set, every push to `main` will auto-deploy to Render.

---

## Manual Server Deployment

### Requirements
- Ubuntu 22.04 LTS (or similar)
- Python 3.11+
- Nginx
- PostgreSQL (optional, SQLite works for small sites)
- SSL certificate (Let's Encrypt)

### Step-by-Step

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install dependencies
sudo apt install -y python3-pip python3-venv nginx postgresql postgresql-contrib certbot python3-certbot-nginx

# 3. Create app user
sudo useradd -m -s /bin/bash roofmasters
sudo mkdir -p /var/www/glasgow-roofmasters
sudo chown roofmasters:roofmasters /var/www/glasgow-roofmasters

# 4. Clone repo (as roofmasters user)
sudo -u roofmasters bash
cd /var/www/glasgow-roofmasters
git clone https://github.com/YOUR_USERNAME/glasgow-roofmasters.git .

# 5. Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# 6. Environment variables
nano .env
# (paste your environment variables)

# 7. Database (if using PostgreSQL)
sudo -u postgres psql -c "CREATE DATABASE roofmasters;"
sudo -u postgres psql -c "CREATE USER roofmasters WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE roofmasters TO roofmasters;"

# 8. Initialize database
flask db init || true
flask db migrate -m "Initial migration"
flask db upgrade

# 9. Systemd service
sudo nano /etc/systemd/system/glasgow-roofmasters.service
```

**Service file content:**
```ini
[Unit]
Description=Glasgow Roofmasters Flask App
After=network.target

[Service]
User=roofmasters
Group=www-data
WorkingDirectory=/var/www/glasgow-roofmasters
Environment="PATH=/var/www/glasgow-roofmasters/venv/bin"
EnvironmentFile=/var/www/glasgow-roofmasters/.env
ExecStart=/var/www/glasgow-roofmasters/venv/bin/gunicorn --workers 4 --bind unix:app.sock -m 007 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start glasgow-roofmasters
sudo systemctl enable glasgow-roofmasters

# 10. Nginx configuration
sudo nano /etc/nginx/sites-available/glasgow-roofmasters
```

**Nginx config:**
```nginx
server {
    listen 80;
    server_name glasgowroofmasters.co.uk www.glasgowroofmasters.co.uk;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/glasgow-roofmasters/app.sock;
    }

    location /static/ {
        alias /var/www/glasgow-roofmasters/app/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /robots.txt {
        alias /var/www/glasgow-roofmasters/app/static/robots.txt;
    }

    location /sitemap.xml {
        alias /var/www/glasgow-roofmasters/app/static/sitemap.xml;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/glasgow-roofmasters /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# 11. SSL with Let's Encrypt
sudo certbot --nginx -d glasgowroofmasters.co.uk -d www.glasgowroofmasters.co.uk
sudo systemctl enable certbot.timer
```

---

## Docker Deployment

```bash
# Build and run
docker-compose up --build -d

# View logs
docker-compose logs -f web

# Stop
docker-compose down

# Production with external DB
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## Custom Domain + SSL

### On Render
1. Go to your service → **Settings** → **Custom Domains**
2. Add `glasgowroofmasters.co.uk` and `www.glasgowroofmasters.co.uk`
3. Render provides auto-managed SSL certificates
4. Update your DNS:
   - A record: `@` → Render IP
   - CNAME: `www` → your-service.onrender.com

### DNS Records Example (Cloudflare/Namecheap)
```
Type    Name            Value                    TTL
A       @               216.24.57.1             Auto
CNAME   www             your-app.onrender.com   Auto
TXT     @               v=spf1 include:_spf...  Auto
```

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | — | Flask secret key (generate strong random string) |
| `DATABASE_URL` | Yes | `sqlite:///...` | Database connection string |
| `MAIL_SERVER` | No | `smtp.gmail.com` | SMTP server |
| `MAIL_PORT` | No | `587` | SMTP port |
| `MAIL_USE_TLS` | No | `true` | Use TLS for email |
| `MAIL_USERNAME` | No | — | SMTP username |
| `MAIL_PASSWORD` | No | — | SMTP password/app password |
| `MAIL_DEFAULT_SENDER` | No | `post@glasgowroofmasters.co.uk` | From address |
| `FLASK_ENV` | No | `production` | Flask environment |
| `PORT` | Auto | `5000` | Server port (Render sets this) |

---

## Post-Deployment Checklist

- [ ] Website loads at custom domain
- [ ] All pages accessible (Home, About, Services, etc.)
- [ ] Contact form submits successfully
- [ ] Free Inspection form submits successfully
- [ ] Admin panel `/admin/requests` shows submissions
- [ ] Email notifications arrive
- [ ] SSL certificate valid (padlock in browser)
- [ ] Mobile responsive test passed
- [ ] Google Search Console verification added
- [ ] Google Analytics tracking code added
- [ ] Facebook Pixel added (if using ads)
