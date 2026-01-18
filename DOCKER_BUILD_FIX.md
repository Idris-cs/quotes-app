# 🐳 Docker Build Fix - January 18, 2026

## Issue Encountered
```
ERROR: failed to build: failed to compute cache key: failed to calculate checksum of ref nsx614ohl089qxmm11unedg50::w1y0jha9wpo6yko9ed0l8kssy: "/2>/dev/null": not found
```

**Root Cause:** Invalid shell redirection syntax in Docker COPY command
```dockerfile
# ❌ WRONG - Docker COPY doesn't support shell operators
COPY frontend/static ./frontend/static/ 2>/dev/null || true
```

---

## Fixes Applied

### Fix #1: Remove Shell Syntax from COPY
```dockerfile
# Before
COPY frontend/static ./frontend/static/ 2>/dev/null || true

# After
COPY frontend/static ./frontend/static/
```

**Why:** Docker's `COPY` instruction doesn't execute in a shell, so redirection operators (`>`, `||`) don't work. If the source directory doesn't exist, the build fails gracefully with proper error message.

### Fix #2: Fix Gunicorn Import Path
```dockerfile
# Before (fails with ModuleNotFoundError: No module named 'app')
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "30", "--access-logfile", "-", "--error-logfile", "-", "backend.wsgi:app"]

# After (adds --chdir to change to backend directory)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "30", "--access-logfile", "-", "--error-logfile", "-", "--chdir", "/app/backend", "wsgi:app"]
```

**Why:** Python needs to be in the `backend/` directory to import the `app` module. Using `--chdir` tells Gunicorn to change directory before trying to import `wsgi:app`.

---

## Build Status

✅ **Docker build succeeds**
```
#15 exporting image
#15 exporting layers
#15 exporting manifest sha256:bd40631b7bfa9db0db4896b6969a63c145ea4f08c342f9ad6e7ce9de836f5aa6
#15 naming to docker.io/library/quotes-app:latest done
```

✅ **Container starts successfully**
```
[2026-01-18 02:08:02 +0000] [1] [INFO] Starting gunicorn 22.0.0
[2026-01-18 02:08:02 +0000] [1] [INFO] Listening at: http://0.0.0.0:8000 (1)
[2026-01-18 02:08:02 +0000] [1] [INFO] Using worker: sync
[2026-01-18 02:08:02 +0000] [7] [INFO] Booting worker with pid: 7
[2026-01-18 02:08:02 +0000] [8] [INFO] Booting worker with pid: 8
```

✅ **Health checks pass** (HTTP 200 responses every 30 seconds)
```
127.0.0.1 - - [18/Jan/2026:02:08:12 +0000] "GET /api/quotes/random HTTP/1.1" 200 140
127.0.0.1 - - [18/Jan/2026:02:08:45 +0000] "GET /api/quotes/random HTTP/1.1" 200 117
127.0.0.1 - - [18/Jan/2026:02:09:19 +0000] "GET /api/quotes/random HTTP/1.1" 200 180
```

---

## Deployment Now Works! 🚀

```bash
# 1. Build image
docker build -f backend/Dockerfile -t quotes-app:latest .
# ✅ SUCCESS - 901MB image created

# 2. Run container
docker-compose up -d
# ✅ SUCCESS - Container starts and stays healthy

# 3. Access app
curl http://localhost:8000/api/quotes/random
# ✅ SUCCESS - Returns random quotes with HTTP 200
```

---

## File Modified
- [backend/Dockerfile](backend/Dockerfile)

## Commit
```
bddf81e Fix Docker build: remove invalid shell syntax from COPY and fix gunicorn import path
```

---

## Summary
✅ Docker image builds successfully
✅ Container starts and runs stably
✅ Health checks working (API responding)
✅ Ready for deployment

**Next Step:** Deploy with `docker-compose up -d`
