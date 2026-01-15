# 🚀 QUICK START - QUOTES APP

## 5-Minute Setup

### 1. Create Supabase Database (2 min)
```bash
# Go to https://app.supabase.com
# Click "New Project"
# Choose a name, password, region
# Wait for it to be created
# Go to Settings → Database → Connection string
# Copy the PostgreSQL URI
```

### 2. Configure Environment (1 min)
```bash
cd c:\Users\Idrissa\quotes-app
cp .env.example .env

# Edit .env and paste your Supabase connection:
# DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@YOUR_HOST.supabase.co:5432/postgres
```

### 3. Install & Run (2 min)
```bash
cd backend
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python init_db.py

python run.py
```

### 4. Open Browser
Visit **http://localhost:5000** 🎉

---

## Test the App

```bash
# In another terminal, with venv activated:
python backend/test_endpoints.py
```

---

## Common Commands

```bash
# Activate virtual environment
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Initialize database
python init_db.py

# Start server
python run.py

# Check database connection
python init_db.py --show-db

# Run tests
python test_endpoints.py
```

---

## Production Deployment

See `SETUP_GUIDE.md` for detailed instructions on:
- Heroku deployment
- Render deployment
- Docker deployment
- Railway deployment

---

## Issues?

Check `ISSUES_AND_FIXES.md` for detailed troubleshooting and all fixes applied to your project.

**Happy coding! 🎉**
