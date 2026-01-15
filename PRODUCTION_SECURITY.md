# Production Security & Performance Guide

## Security Configuration

### 1. Environment Variables
All sensitive data must be environment variables, never hardcoded:

**Required for Production:**
```
DATABASE_URL        → Supabase PostgreSQL connection string
FLASK_ENV          → Set to 'production'
FLASK_DEBUG        → Set to False
SECRET_KEY         → Unique 32+ character random string
```

**How to generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. HTTPS/TLS Configuration

The application is now production-ready with:
- ✅ Secure session cookies enabled
- ✅ HTTPOnly flag on cookies (prevents XSS attacks)
- ✅ SameSite=Lax CSRF protection
- ✅ Debug mode disabled in production

For HTTPS deployment:
```python
# Automatically enabled when deployed with HTTPS
SESSION_COOKIE_SECURE = True
```

### 3. CORS Configuration
Current setup allows cross-origin requests to `/api/*` endpoints.

For production, restrict to your domain:
```python
# In backend/app/__init__.py
CORS(app, resources={
    r"/api/*": {"origins": ["https://yourdomain.com"]}
})
```

### 4. Secret Key Rotation
Change SECRET_KEY periodically (recommended: every 3-6 months):
1. Generate new key: `python -c "import secrets; print(secrets.token_hex(32))"`
2. Update environment variable
3. Restart application
4. Users sessions will be invalidated (they'll re-login)

---

## Performance Optimization

### 1. Database Connection Pooling
SQLAlchemy pool settings for production:

```python
# In config.py (optional customization)
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size": 10,
    "pool_recycle": 3600,
    "pool_pre_ping": True,
    "max_overflow": 20,
}
```

Current defaults:
- Pool size: 5 connections
- Recycle: 1 hour (prevents timeout issues)
- Pre-ping: Enabled (validates connections)

### 2. Gunicorn Worker Configuration
The Dockerfile uses these settings:
```
--workers 4        → CPU cores typically
--threads 2        → Threads per worker (8 total threads)
--timeout 60       → Request timeout
```

For different workloads:
```bash
# High concurrency (many simultaneous users)
gunicorn --workers 8 --threads 4 --worker-class gthread wsgi:app

# CPU-intensive tasks
gunicorn --workers $(nproc) --worker-class sync wsgi:app

# Low resource environment
gunicorn --workers 2 --threads 1 wsgi:app
```

### 3. Caching Strategy

**Database Queries (recommended addition):**
```python
# Cache random quotes for 1 hour
@cache.cached(timeout=3600)
def get_random_quote():
    return Quote.query.order_by(func.random()).first()
```

**Static Files:**
- Served with cache headers
- Set browser cache to 30 days for versioned files
- Use CDN (CloudFlare) for geographic distribution

### 4. Logging & Monitoring

Current logs visible via:
```bash
docker-compose logs -f web
```

For production, add external logging:
```python
# In app/__init__.py
import logging
from logging.handlers import SysLogHandler

handler = SysLogHandler()
app.logger.addHandler(handler)
```

Services to integrate:
- **Error Tracking**: Sentry, DataDog
- **Monitoring**: New Relic, CloudWatch
- **Logging**: ELK Stack, Splunk, CloudWatch

---

## Deployment Platforms

### Heroku
```bash
# Create app
heroku create quotes-app

# Set environment variables
heroku config:set FLASK_ENV=production \
  FLASK_DEBUG=False \
  SECRET_KEY=<your-key> \
  DATABASE_URL=<your-supabase-url>

# Deploy
git push heroku main
```

### DigitalOcean App Platform
1. Connect GitHub repository
2. Set environment variables in dashboard
3. Configure health check: `/api/quotes/random`
4. Deploy

### AWS Elastic Container Service (ECS)
1. Push image to ECR
2. Create ECS task definition with environment variables
3. Create ECS service pointing to load balancer
4. Configure auto-scaling

### Google Cloud Run
```bash
gcloud run deploy quotes-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars FLASK_ENV=production,DATABASE_URL=$DATABASE_URL
```

### DigitalOcean App Platform (Docker)
```bash
# Push image
docker tag quotes-app:latest registry.digitalocean.com/your-registry/quotes-app:latest
docker push registry.digitalocean.com/your-registry/quotes-app:latest
```

---

## Database Optimization

### 1. Indexes
For faster queries, ensure these columns are indexed:
```sql
-- Already created by SQLAlchemy
CREATE INDEX idx_quotes_category_id ON quotes(category_id);
CREATE INDEX idx_quotes_author ON quotes(author);
CREATE INDEX idx_categories_slug ON categories(slug);

-- Optional: for search performance
CREATE INDEX idx_quotes_text_search ON quotes USING GIN(to_tsvector('english', text));
```

### 2. Connection Limits
Supabase free tier: 2 connections
Supabase paid tier: Scales with plan

Monitor via Supabase dashboard:
- Active connections
- Connection errors
- Query performance

### 3. Backup Strategy
Supabase handles automatic backups:
- Daily backups (free tier)
- Point-in-time recovery (premium)

Manual backup (optional):
```bash
# Export data
pg_dump $DATABASE_URL > backup.sql

# Restore
psql $DATABASE_URL < backup.sql
```

---

## Monitoring Checklist

### Daily
- [ ] Application is accessible
- [ ] API endpoints responding
- [ ] No error spikes in logs
- [ ] Database queries performing normally

### Weekly
- [ ] Review error logs for patterns
- [ ] Check disk space usage
- [ ] Verify backups completed
- [ ] Monitor API response times

### Monthly
- [ ] Review security logs
- [ ] Update dependencies
- [ ] Optimize slow queries
- [ ] Plan capacity scaling

---

## Incident Response

### Application Down
1. Check container status: `docker-compose ps`
2. View logs: `docker-compose logs web`
3. Restart: `docker-compose restart web`
4. If persistent, check database connectivity: `python backend/main.py`

### Database Connection Issues
1. Verify DATABASE_URL in environment variables
2. Check Supabase dashboard for service status
3. Test connection: `psql $DATABASE_URL`
4. Check connection limit not exceeded
5. Review database logs in Supabase

### Performance Degradation
1. Check active connections: `SELECT count(*) FROM pg_stat_activity;`
2. Identify slow queries: Check Supabase query logs
3. Scale workers: Increase gunicorn workers
4. Clear application cache if applicable

### Security Breach
1. Rotate SECRET_KEY immediately
2. Review database access logs
3. Check for unauthorized changes
4. Consider resetting Supabase password
5. Notify team and stakeholders
6. Post-incident review

---

## Compliance & Standards

✅ **OWASP Top 10 Mitigation:**
- CSRF Protection (SameSite cookies)
- XSS Prevention (HTTPOnly cookies, Content-Security-Policy)
- SQL Injection Prevention (SQLAlchemy ORM)
- Secure Authentication (SECRET_KEY encryption)

✅ **Data Protection:**
- Database encrypted by Supabase
- HTTPS recommended for frontend
- No sensitive data in logs
- Secure password storage

✅ **API Best Practices:**
- RESTful endpoint design
- Proper HTTP status codes
- Error response consistency
- CORS properly configured

---

## Support & Escalation

**Issue**: Application not starting
→ Check: Docker logs, environment variables, database connectivity

**Issue**: Slow performance
→ Check: Database query logs, connection pool, worker count

**Issue**: Database errors
→ Check: Supabase status, connection limits, disk space

**Escalation**: Contact Supabase support if database issues persist

---

**Last Updated**: January 15, 2026
**Recommended Review**: Quarterly

