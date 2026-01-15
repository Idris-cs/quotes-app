# Production Deployment Checklist

## Pre-Deployment ✅

### Security
- [ ] Generate secure SECRET_KEY: `python -c "import secrets; print(secrets.token_hex(32))"`
- [ ] Update `.env` with production values (not committed to git)
- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=False`
- [ ] Review `.env.production` template for all required variables
- [ ] Verify Supabase credentials (host, user, password, port, database)
- [ ] Enable HTTPS/TLS for database connection
- [ ] Configure CORS for your domain

### Database
- [ ] Test connection: `python backend/main.py` → "Connection successful!"
- [ ] Verify Supabase database is accessible
- [ ] Check database user permissions (create tables, insert data)
- [ ] Set up automatic backups (Supabase dashboard)
- [ ] Test init_db script: `python backend/init_db.py`

### Application
- [ ] All code tested locally with production config
- [ ] Environment variables validated
- [ ] Static files (CSS, JS) accessible and working
- [ ] API endpoints responding correctly
- [ ] No debug output in logs
- [ ] Error handling properly configured

### Dependencies
- [ ] `requirements.txt` up to date
- [ ] All packages pinned to specific versions
- [ ] No development dependencies in production
- [ ] Gunicorn included (for WSGI serving)

---

## Docker Deployment ✅

### Docker Setup
- [ ] Dockerfile created and tested locally
- [ ] Docker image builds without errors: `docker build -f backend/Dockerfile -t quotes-app:latest .`
- [ ] docker-compose.yml configured with production settings
- [ ] Environment variables properly referenced in docker-compose.yml
- [ ] Health checks configured and working

### Build & Test
- [ ] Build image: `docker build -f backend/Dockerfile -t quotes-app:latest .`
- [ ] Test image locally: `docker run -p 8000:8000 --env-file .env quotes-app:latest`
- [ ] Verify API endpoints: `curl http://localhost:8000/api/quotes/random`
- [ ] Check static files load correctly
- [ ] Database connections work inside container

### Deployment
- [ ] Push Docker image to registry (if using cloud platform)
- [ ] Deploy container: `docker-compose up -d`
- [ ] Verify container is running: `docker-compose ps`
- [ ] Check logs for errors: `docker-compose logs web`
- [ ] Test health endpoint: `curl http://localhost:8000/api/quotes/random`

---

## Post-Deployment ✅

### Verification
- [ ] Application accessible at your domain
- [ ] Web UI loads without errors
- [ ] API endpoints respond correctly
- [ ] Static files (CSS, images) load properly
- [ ] Database queries working
- [ ] Random quote endpoint works: `/api/quotes/random`
- [ ] Category listing works: `/api/category/<slug>/quotes`
- [ ] Search functionality works: `/api/search?q=<query>`
- [ ] No console errors in browser
- [ ] Performance acceptable (page load < 2s)

### Monitoring
- [ ] Set up error logging/monitoring (e.g., Sentry)
- [ ] Monitor container health: `docker-compose ps`
- [ ] Check logs regularly for errors: `docker-compose logs web`
- [ ] Set up alerts for container restarts
- [ ] Monitor database connection status
- [ ] Track resource usage (CPU, memory)

### Security Verification
- [ ] HTTPS/TLS enabled (if using custom domain)
- [ ] CORS headers correct (no overly permissive settings)
- [ ] No sensitive data in logs or responses
- [ ] Rate limiting configured (if needed)
- [ ] Database credentials not exposed in any way
- [ ] .env file inaccessible to public
- [ ] No debug information exposed

---

## Performance Optimization ✅

- [ ] Database queries optimized (check query logs)
- [ ] Connection pooling configured
- [ ] Static files cached (browser cache headers set)
- [ ] API responses compressed (gzip enabled)
- [ ] Gunicorn workers appropriately sized
- [ ] Database indexes created for frequent queries

---

## Backup & Disaster Recovery ✅

- [ ] Database backups automated (Supabase)
- [ ] Test restore procedure documented
- [ ] Application code backed up (git)
- [ ] .env values securely stored (password manager/vault)
- [ ] Rollback procedure documented and tested
- [ ] Contact list for emergency support

---

## Documentation ✅

- [ ] DEPLOYMENT_GUIDE.md updated
- [ ] Environment variables documented
- [ ] Database schema documented
- [ ] API endpoints documented
- [ ] Troubleshooting guide provided
- [ ] Team has access to documentation

---

## Sign-Off

| Role | Name | Date | Sign |
|------|------|------|------|
| Developer | | | |
| DevOps/Ops | | | |
| Security Review | | | |
| Manager | | | |

---

## Post-Launch Tasks

1. **Week 1**
   - [ ] Monitor logs for errors
   - [ ] Verify all features working
   - [ ] Confirm database backups running
   - [ ] Check performance metrics

2. **Week 2**
   - [ ] User acceptance testing
   - [ ] Gather feedback
   - [ ] Optimize based on usage patterns
   - [ ] Document any issues/resolutions

3. **Ongoing**
   - [ ] Regular security updates
   - [ ] Database maintenance
   - [ ] Performance monitoring
   - [ ] Feature enhancements

---

**Deployment Date**: _______________
**Deployed By**: _______________
**Environment**: Production

