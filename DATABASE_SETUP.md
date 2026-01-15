# Database Setup Guide for Quotes App

## Quick Start with Supabase

### 1. Create a Supabase Project
1. Go to [https://app.supabase.com](https://app.supabase.com)
2. Click "New project" and fill in the details
3. Wait for the project to be created (usually 2-3 minutes)

### 2. Get Your Connection String
1. In your Supabase project, go to **Settings** → **Database** → **Connection string**
2. Select **URI** tab
3. Copy the connection string

### 3. Configure Your .env File
```bash
cp .env.example .env
```

Edit `.env` and replace:
```
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@[YOUR-HOST].supabase.co:5432/postgres
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

### 4. Initialize the Database
```bash
# From backend directory
python init_db.py
```

This will:
- Create all necessary tables (Category, Quote)
- Scrape quotes from quotable.io API
- Populate 9 categories with 100+ quotes each
- Setup indexes for performance

### 5. Test the Connection
```bash
python init_db.py --show-db
```

This shows your masked DATABASE_URL to verify the connection is configured correctly.

## Database Schema

### Categories Table
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    icon VARCHAR(50) DEFAULT 'quote',
    quote_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Quotes Table
```sql
CREATE TABLE quotes (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    author VARCHAR(255),
    tags TEXT,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    source VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_quotes_category ON quotes(category_id);
CREATE INDEX idx_quotes_text ON quotes USING GIN(to_tsvector('english', text));
```

## Troubleshooting

### Connection Timeout
- Ensure Supabase project is running
- Check your network/firewall allows PostgreSQL connections
- Verify DATABASE_URL is correct

### "Already Populated" Error
The script checks if data exists before scraping. To reset:
```bash
# WARNING: This deletes all data!
# From backend directory with activated venv:
python -c "from app import create_app, db; app = create_app(); db.drop_all()"
python init_db.py
```

### SSL Certificate Error
If you get SSL errors with Supabase on Windows:
```python
# This is already handled in scraper.py with:
session.verify = False  # Only for development!
```

For production, ensure proper SSL certificates are installed.

## Local Development Alternative (SQLite)

If you don't have Supabase yet, the app falls back to SQLite:
```bash
# Just skip setting DATABASE_URL
python init_db.py
```

This creates `backend/quotes.db` automatically.

**Important**: SQLite is fine for development but switch to Supabase for production.

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| DATABASE_URL | sqlite:///:memory: | PostgreSQL or SQLite connection string |
| FLASK_ENV | development | Set to 'production' for deployment |
| FLASK_DEBUG | False | Enable debug mode (never in production) |
| SECRET_KEY | dev-key | Change this in production! |
| DB_CONNECT_RETRIES | 5 | Connection retry attempts |
| DB_CONNECT_BASE_DELAY | 1.0 | Base delay between retries in seconds |

## Next Steps

1. ✅ Initialize database with `python init_db.py`
2. ✅ Run the app with `python run.py`
3. ✅ Visit http://localhost:5000
4. ✅ Check the API endpoints work: http://localhost:5000/api/quotes/random
