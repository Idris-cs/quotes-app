# 🚀 Render Deployment Guide

Render is a modern cloud platform that's similar to Heroku but with better pricing and features. It offers a free tier that actually works!

## Why Render?

✅ Free tier includes PostgreSQL database  
✅ Automatic HTTPS and SSL  
✅ Native Docker support  
✅ Better free tier than Heroku  
✅ Simple GitHub integration  
✅ Zero cold starts on paid plans  
✅ $7/month for production-grade hosting  

---

## Step-by-Step Deployment to Render

### Prerequisites
- GitHub account with your `quotes-app` repo pushed
- Render account (sign up at https://render.com)

### Step 1: Create render.yaml Configuration

Create this file in your project root:

```yaml
services:
  - type: web
    name: quotes-app
    env: docker
    plan: free
    branch: main
    healthCheckPath: /api/quotes/random
    envVars:
      - key: FLASK_ENV
        value: production
      - key: FLASK_DEBUG
        value: false
      - key: PORT
        value: 8000
      - key: SECRET_KEY
        generateValue: true
    envVarFiles:
      - file: .env.render
```

### Step 2: Create .env.render File

Create `.env.render` (you'll fill this in Render dashboard later):

```env
# Add to Render dashboard environment variables
DATABASE_URL=${DATABASE_URL}
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=${SECRET_KEY}
PORT=8000
```

**Note:** Don't commit actual credentials. Set them in Render dashboard.

### Step 3: Update docker-compose.yml (Optional)

If using docker-compose for local dev, no changes needed. Render will use Dockerfile directly.

### Step 4: Push to GitHub

```bash
cd /c/Users/Idrissa/quotes-app
git add render.yaml .env.render
git commit -m "Add Render deployment configuration"
git push origin main
```

### Step 5: Connect to Render

1. Go to https://render.com and sign in
2. Click "New +" → "Web Service"
3. Select "Build and deploy from a Git repository"
4. Connect your GitHub account
5. Select `quotes-app` repository
6. Render will auto-detect `render.yaml`
7. Click "Create Web Service"

### Step 6: Configure Environment Variables

In Render dashboard for your service:

1. Go to "Environment" tab
2. Add these variables:
   ```
   DATABASE_URL=postgresql://user:password@host:port/database
   FLASK_ENV=production
   FLASK_DEBUG=False
   SECRET_KEY=<generate-a-random-secret-key>
   PORT=8000
   ```

3. Get your `DATABASE_URL` from Supabase:
   - Go to Supabase dashboard
   - Project Settings → Database
   - Connection string (URI) → Copy full URL
   - Replace in Render environment variables

### Step 7: Deploy!

1. Click "Deploy" button in Render dashboard
2. Watch the deployment logs
3. Once deployed, you'll get a URL like: `https://quotes-app-xxxxx.onrender.com`

---

## Testing Your Render Deployment

```bash
# Test API endpoint
curl https://quotes-app-xxxxx.onrender.com/api/quotes/random

# Test homepage
curl https://quotes-app-xxxxx.onrender.com/

# Check health
curl https://quotes-app-xxxxx.onrender.com/api/quotes/random -I
```

Expected response:
```
HTTP/2 200
content-type: application/json
```

---

## Free Tier Limitations & Upgrades

### Free Tier Includes
- ✅ Hosting
- ✅ HTTPS/SSL
- ✅ GitHub integration
- ✅ Automatic deploys
- ✅ PostgreSQL database (500MB)

### Free Tier Limitations
- ⚠️ Spins down after 15 min inactivity
- ⚠️ Max 0.5GB RAM
- ⚠️ Shared CPU

### Upgrade to Starter ($7/month)
- ✅ Always running
- ✅ Dedicated CPU
- ✅ 2GB RAM
- ✅ Better performance
- ✅ No cold starts

**Recommendation:** Start free, upgrade to $7/month once confident

---

## Automatic Deployments

Render automatically deploys when you:
```bash
git push origin main
```

The deployment will:
1. Pull latest code
2. Build Docker image
3. Run migrations (if needed)
4. Start container
5. Run health check
6. Route traffic to new version

You can monitor in Render dashboard → "Logs"

---

## Custom Domain (Optional)

1. In Render dashboard:
   - Go to Settings
   - Add Custom Domain
   - Point your domain's CNAME to Render
   - Wait for SSL certificate

2. Your app will be at: `https://yourdomain.com`

---

## Troubleshooting

### Build Fails
```bash
# Check Render logs
# Go to Render dashboard → Logs
# Usually issue with missing environment variables
```

### App Crashes on Deploy
```bash
# Common causes:
# 1. Missing environment variables
# 2. Database connection string invalid
# 3. Port mismatch

# Check logs in Render dashboard
```

### Slow Response Times
```bash
# If on free tier:
# - Might be cold start (15 min inactivity)
# - Upgrade to Starter plan ($7/month) to avoid this
```

### Database Connection Error
```bash
# Verify DATABASE_URL format:
# postgresql://user:password@host:port/database

# Check Supabase is accepting connections
# Verify IP whitelist (if any)
```

---

## Monitoring & Logs

1. **Real-time Logs**: Render dashboard → Logs tab
2. **Error Tracking**: Set up Sentry for better error tracking
3. **Performance**: Monitor in Render dashboard → Metrics

---

## Environment Variables Reference

```env
# Required
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=<your-secret-key>

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
PORT=8000

# Optional
DB_CONNECT_RETRIES=5
DB_CONNECT_BASE_DELAY=1.0
```

---

## Cost Breakdown

| Component | Cost |
|-----------|------|
| Web Service (Starter) | $7/month |
| PostgreSQL (included) | Free |
| Custom Domain | $10-15/year |
| SSL/HTTPS | Free (auto) |
| **Total** | **~$7/month** |

---

## Next Steps After Render Deployment

1. ✅ Verify app works on Render
2. ✅ Add custom domain
3. ✅ Set up monitoring (Sentry)
4. ✅ Configure automatic backups
5. ✅ Add rate limiting
6. ✅ Monitor performance
7. ✅ Plan feature roadmap

---

## Render Resources

- **Render Docs:** https://render.com/docs
- **Docker Deploys:** https://render.com/docs/docker
- **Environment Variables:** https://render.com/docs/environment-variables
- **PostgreSQL:** https://render.com/docs/databases

---

## Quick Reference

```bash
# Local testing (before pushing to Render)
docker-compose up -d
curl http://localhost:8000/api/quotes/random

# Push to Render
git push origin main

# Monitor deployment
# Go to https://render.com → Your Service → Logs

# View deployed app
https://quotes-app-xxxxx.onrender.com
```

---

**Ready to deploy to Render? Follow the 7 steps above!** 🚀
