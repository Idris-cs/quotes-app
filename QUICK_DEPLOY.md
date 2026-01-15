# Quotes App - Quick Deployment Reference

## 🚀 30-Second Deploy

```bash
# 1. Generate SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# 2. Configure environment
cp backend/.env.production .env
# Edit .env with your Supabase credentials

# 3. Deploy
docker-compose up -d

# 4. Verify
curl http://localhost:8000/api/quotes/random
```

---

## 📋 Checklist

Before deploying, ensure:
- [ ] Supabase project created and credentials obtained
- [ ] .env file configured (not committed to git)
- [ ] `python backend/main.py` returns "Connection successful!"
- [ ] `python backend/init_db.py` completes without errors
- [ ] Docker and docker-compose installed

---

## 🔒 Production Checklist

- [ ] FLASK_ENV=production
- [ ] FLASK_DEBUG=False
- [ ] SECRET_KEY is unique and strong
- [ ] DATABASE_URL uses Supabase credentials
- [ ] .env is in .gitignore (never commit secrets!)
- [ ] HTTPS/TLS enabled
- [ ] Monitoring configured
- [ ] Backups enabled

---

## 📊 Key Files

| File | Purpose |
|------|---------|
| `.env` | Production configuration (secrets - don't commit) |
| `docker-compose.yml` | Container orchestration |
| `backend/Dockerfile` | Docker image definition |
| `backend/config.py` | Flask configuration |
| `backend/wsgi.py` | WSGI entry point for gunicorn |

---

## 🐳 Docker Commands

```bash
# Build image
docker build -f backend/Dockerfile -t quotes-app:latest .

# Start containers
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop containers
docker-compose down

# Restart service
docker-compose restart web

# Show status
docker-compose ps
```

---

## 🧪 Testing

```bash
# Direct connection test
python backend/main.py
# Expected: Connection successful!

# Initialize database
python backend/init_db.py
# Expected: Database populated successfully!

# Test API
curl http://localhost:8000/api/quotes/random
# Expected: JSON quote response

# Test web UI
curl http://localhost:8000/
# Expected: HTML page
```

---

## 🔍 Monitoring

```bash
# View real-time logs
docker-compose logs -f web

# Check container status
docker-compose ps

# View specific service logs
docker-compose logs web --tail=50

# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}"
```

---

## 🚨 Troubleshooting

**Container won't start?**
```bash
docker-compose logs web
# Check .env file, DATABASE_URL format
```

**Database connection failed?**
```bash
python backend/main.py
# Verify Supabase credentials, network connectivity
```

**Static files not loading?**
```bash
# Verify path: frontend/templates/templates/static/styles.css
docker-compose restart web  # Restart after fixing
```

**Port already in use?**
```bash
# Change port in docker-compose.yml
# Or: docker-compose up -d -e PORT=9000
```

---

## 📚 Full Documentation

- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Complete deployment walkthrough
- **[DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)** - Verification checklist
- **[PRODUCTION_SECURITY.md](./PRODUCTION_SECURITY.md)** - Security & performance
- **[DEPLOYMENT_READY.md](./DEPLOYMENT_READY.md)** - Full summary

---

## 🔐 Environment Variables

```bash
# Required
DATABASE_URL=postgresql://user:pass@host:6543/db
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-32-char-random-string

# Optional
PORT=8000
DB_CONNECT_RETRIES=5
```

---

## ⚡ Performance Tuning

**More workers (high traffic)**
```dockerfile
CMD ["gunicorn", "--workers", "8", "--threads", "4", "wsgi:app"]
```

**Less resources (limited VM)**
```dockerfile
CMD ["gunicorn", "--workers", "2", "--threads", "1", "wsgi:app"]
```

---

## 🆘 Support

| Issue | Solution |
|-------|----------|
| Connection failed | Check `python main.py` output |
| Slow performance | Monitor logs, increase workers |
| Database errors | Verify Supabase status/credentials |
| Container crashes | Check `docker-compose logs web` |
| Port conflict | Change PORT in .env or docker-compose.yml |

---

## 🎯 Success Indicators

✅ Container running: `docker-compose ps` shows "Up"  
✅ Health check passing: Endpoint responds in <1s  
✅ Database connected: `python main.py` → "Connection successful!"  
✅ API working: `curl http://localhost:8000/api/quotes/random` returns quote  
✅ Web UI loads: `curl http://localhost:8000/` returns HTML  

---

**Ready for deployment!** 🚀

Last updated: January 15, 2026

