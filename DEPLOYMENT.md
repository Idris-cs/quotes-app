# Deployment Guide

## Deploying Quotes App to Production

This guide covers deploying the Quotes App to a production server.

## Prerequisites

- Ubuntu/Debian server or similar Linux distribution
- SSH access to server
- Python 3.8+
- MySQL Server installed
- Domain name (optional)

## Step 1: Server Setup

### Install System Dependencies

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv python3-dev mysql-server nginx supervisor
```

### Create Application User

```bash
sudo useradd -m -s /bin/bash quotesapp
sudo su - quotesapp
```

## Step 2: Deploy Application

### Clone/Upload Code

```bash
# Option 1: Clone from Git
git clone <your-repo> ~/quotes-app
cd ~/quotes-app

# Option 2: Upload via SCP
# From local: scp -r quotes-app/* quotesapp@server:/home/quotesapp/quotes-app/
```

### Setup Virtual Environment

```bash
cd ~/quotes-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 3: Configure Database

### Create Database

```bash
sudo mysql -u root -p
```

```sql
CREATE DATABASE quotes_db_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'quotesapp'@'localhost' IDENTIFIED BY 'strong-password-here';
GRANT ALL PRIVILEGES ON quotes_db_prod.* TO 'quotesapp'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Update Configuration

Edit `config.py`:

```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'generate-strong-key-here')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://quotesapp:strong-password-here@localhost:3306/quotes_db_prod'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = 3600
```

Or use environment variables:

```bash
export SECRET_KEY='your-secret-key-here'
export DATABASE_URL='mysql+pymysql://quotesapp:password@localhost:3306/quotes_db_prod'
```

### Initialize Database

```bash
cd ~/quotes-app
source venv/bin/activate
python init_db.py
```

## Step 4: Setup Gunicorn

### Create Gunicorn Config

```bash
cat > ~/quotes-app/gunicorn_config.py << 'EOF'
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 60
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
EOF
```

### Test Gunicorn

```bash
cd ~/quotes-app
source venv/bin/activate
gunicorn -c gunicorn_config.py wsgi:app
```

Press Ctrl+C to stop.

## Step 5: Setup Supervisor

### Create Supervisor Config

```bash
sudo nano /etc/supervisor/conf.d/quotes-app.conf
```

Paste this:

```ini
[program:quotes-app]
directory=/home/quotesapp/quotes-app
command=/home/quotesapp/quotes-app/venv/bin/gunicorn -c gunicorn_config.py wsgi:app
user=quotesapp
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/quotesapp/quotes-app/logs/gunicorn.log
environment=PATH="/home/quotesapp/quotes-app/venv/bin",SECRET_KEY="your-secret-key",DATABASE_URL="mysql+pymysql://quotesapp:password@localhost:3306/quotes_db_prod"
```

### Enable Supervisor

```bash
sudo mkdir -p /home/quotesapp/quotes-app/logs
sudo chown -R quotesapp:quotesapp /home/quotesapp/quotes-app/logs
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start quotes-app
sudo supervisorctl status
```

## Step 6: Setup Nginx

### Create Nginx Config

```bash
sudo nano /etc/nginx/sites-available/quotes-app
```

Paste this:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # Redirect HTTP to HTTPS (optional, requires SSL)
    # return 301 https://$server_name$request_uri;

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    location /static/ {
        alias /home/quotesapp/quotes-app/app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### Enable Nginx Site

```bash
sudo ln -s /etc/nginx/sites-available/quotes-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 7: SSL Certificate (Let's Encrypt)

### Install Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com -d www.your-domain.com
```

### Update Nginx Config for HTTPS

```bash
sudo nano /etc/nginx/sites-available/quotes-app
```

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    location /static/ {
        alias /home/quotesapp/quotes-app/app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### Restart Nginx

```bash
sudo systemctl restart nginx
```

## Step 8: Monitoring & Maintenance

### Check Logs

```bash
# Supervisor logs
tail -f /home/quotesapp/quotes-app/logs/gunicorn.log

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Monitor Service

```bash
# Check service status
sudo supervisorctl status quotes-app

# Restart if needed
sudo supervisorctl restart quotes-app

# Restart Nginx
sudo systemctl restart nginx
```

### Auto-renew SSL

```bash
# Test renewal
sudo certbot renew --dry-run

# Create cron job (usually automatic)
sudo systemctl enable certbot.timer
```

## Step 9: Backup Strategy

### Daily Database Backup

```bash
sudo nano /usr/local/bin/backup-quotes-db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/home/quotesapp/backups"
DB_NAME="quotes_db_prod"
DB_USER="quotesapp"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
mysqldump -u $DB_USER -p$DB_PASSWORD $DB_NAME | gzip > $BACKUP_DIR/quotes_db_$TIMESTAMP.sql.gz

# Keep only last 7 days
find $BACKUP_DIR -name "quotes_db_*.sql.gz" -mtime +7 -delete
```

```bash
sudo chmod +x /usr/local/bin/backup-quotes-db.sh
sudo crontab -e
# Add: 0 2 * * * /usr/local/bin/backup-quotes-db.sh
```

## Performance Optimization

### Enable Caching

Edit `config.py`:

```python
class Config:
    # ... other config ...
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year
```

### Database Indexing

```sql
-- Already included in models, but verify:
CREATE INDEX idx_category_slug ON categories(slug);
CREATE INDEX idx_quote_category ON quotes(category_id);
CREATE INDEX idx_quote_text ON quotes(text(100));
```

### Setup Redis Cache (Optional)

```bash
sudo apt install redis-server
pip install redis
```

## Troubleshooting

### App won't start

```bash
# Check syntax
python -m py_compile wsgi.py

# Test imports
source venv/bin/activate
python -c "from app import create_app; create_app()"
```

### Database connection error

```bash
# Test connection
mysql -u quotesapp -p -h localhost -e "USE quotes_db_prod; SELECT COUNT(*) FROM quotes;"
```

### Port 8000 already in use

```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

### Nginx 502 Bad Gateway

```bash
# Check if Gunicorn is running
sudo supervisorctl status quotes-app

# Check logs
tail -f /home/quotesapp/quotes-app/logs/gunicorn.log
```

## Summary

Your Quotes App is now deployed! 

- **URL**: https://your-domain.com
- **Admin SSH**: `ssh quotesapp@server-ip`
- **Monitoring**: `sudo supervisorctl status quotes-app`
- **Logs**: `/home/quotesapp/quotes-app/logs/gunicorn.log`

Keep the app updated and monitor for any issues!
