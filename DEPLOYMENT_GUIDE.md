# Deployment Guide - Quotes App

## Overview
This guide walks you through deploying the Quotes App to production using Docker and Supabase PostgreSQL.

## Prerequisites
- Docker and Docker Compose installed
- Supabase account with PostgreSQL database
- Your Supabase credentials (host, user, password, port, database name)

## Step 1: Prepare Production Environment

### 1.1 Generate a Secure SECRET_KEY
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Copy the output for use in the next step.

### 1.2 Configure Production Environment
Copy the example production config:
```bash
cp backend/.env.production .env
```

Then edit `.env` with your actual values:
```dotenv
# Database credentials from Supabase
DATABASE_URL=postgresql://postgres.YOUR_PROJECT_ID:YOUR_PASSWORD@YOUR_HOST:6543/postgres
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<paste-your-generated-key-here>
```

**⚠️ CRITICAL SECURITY NOTES:**
- Never commit `.env` to git (it's in .gitignore)
- Use unique, strong passwords from Supabase
- Change SECRET_KEY to your generated value
- Rotate credentials periodically
- Keep .env file private and restricted to authorized personnel

### 1.3 Verify Database Connectivity
```bash
# From backend directory
python main.py
```
Expected output: `Connection successful!`

## Step 2: Initialize Database (First-Time Only)

Run migrations and seed data:
```bash
cd backend
python init_db.py
```

This will:
- Create database tables (categories, quotes)
- Populate with quote data from API
- Skip if data already exists (idempotent)

## Step 3: Build and Deploy with Docker

### 3.1 Build the Docker Image
```bash
docker build -f backend/Dockerfile -t quotes-app:latest .
```

### 3.2 Run with Docker Compose
```bash
docker-compose up -d
```

This will:
- Build the image (if not already built)
- Start the application on port 8000
- Enable automatic restart on failure
- Set up health checks

### 3.3 Verify Deployment
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f web

# Test the API
curl http://localhost:8000/api/quotes/random
```

## Step 4: Access Your Application

### Local Docker
- **Web UI**: http://localhost:8000
- **API**: http://localhost:8000/api/quotes/random

### Cloud Deployment (e.g., DigitalOcean, AWS, Heroku)
- Update domain/port based on your platform
- Set up reverse proxy (nginx) if needed
- Enable SSL/TLS certificates (Let's Encrypt)

## Step 5: Production Configuration

### Environment Variables (for your platform)
Configure these in your deployment platform's environment settings:

```
DATABASE_URL = postgresql://postgres.xyz:password@aws-1-us-east-1.pooler.supabase.com:6543/postgres
FLASK_ENV = production
FLASK_DEBUG = False
SECRET_KEY = <your-secure-key>
DB_CONNECT_RETRIES = 5
DB_CONNECT_BASE_DELAY = 1.0
```

### Reverse Proxy Setup (nginx example)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Troubleshooting

### Database Connection Issues
```bash
# Check database connectivity
python backend/main.py

# View detailed logs
docker-compose logs web
```

### Static Files Not Loading
- Verify `frontend/templates/templates/static/` directory exists
- Check Flask static folder configuration in `backend/app/__init__.py`
- Clear browser cache (Ctrl+F5)

### Container Won't Start
```bash
# Check logs
docker-compose logs web

# Verify environment variables
docker-compose config

# Rebuild image
docker-compose build --no-cache
```

### Port Already in Use
```bash
# Change port in docker-compose.yml or run command
docker-compose up -d -e PORT=9000
```

## Maintenance

### Update Application
```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose up -d --build
```

### Database Backups
With Supabase, backups are handled automatically. Access them through the Supabase dashboard.

### Monitoring
- Use `docker-compose logs` for real-time logs
- Monitor health checks in docker-compose ps output
- Set up alerts for container restarts (if using orchestration)

### Scaling
For higher traffic:
1. Increase worker processes: `--workers 8` in Dockerfile CMD
2. Use a load balancer (nginx, cloud provider)
3. Implement caching layer (Redis)
4. Scale database connections if needed

## Security Checklist

- [x] SECRET_KEY is unique and strong (32+ characters)
- [x] FLASK_ENV is set to 'production'
- [x] FLASK_DEBUG is False
- [x] DATABASE_URL uses HTTPS/TLS-enabled host
- [x] .env file is in .gitignore
- [x] SSL/TLS certificates configured (if using custom domain)
- [x] Security headers configured (consider adding to Flask app)
- [x] CORS properly configured for allowed origins
- [x] Rate limiting implemented (optional, for public APIs)
- [x] Logging and monitoring enabled

## Performance Optimization

1. **Caching**: Implement Redis for session/quote caching
2. **CDN**: Serve static files via CloudFlare or similar
3. **Database Indexing**: Ensure proper indexes on frequently queried columns
4. **Connection Pooling**: Adjust SQLAlchemy pool settings for high load

## Rollback Procedure

If deployment fails:
```bash
# Stop current deployment
docker-compose down

# Switch to previous version
git checkout <previous-commit>

# Rebuild and restart
docker-compose up -d --build
```

## Support & Logs

For issues, check:
1. Docker logs: `docker-compose logs web`
2. Database connection: `python backend/main.py`
3. Application configuration: Verify all environment variables set correctly
4. Supabase dashboard: Check database status and connection limits

---

**Last Updated**: January 15, 2026
**Version**: 1.0
