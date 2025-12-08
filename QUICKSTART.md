# Quick Start Guide

## Get the App Running in 5 Minutes

### 1. Prerequisites
- ✅ Python 3.8+ installed
- ✅ MySQL Server running
- ✅ Command line/Terminal access

### 2. Setup Database

**MySQL Command Line:**
```bash
mysql -u root -p
```

**Then paste this:**
```sql
CREATE DATABASE quotes_db;
ALTER DATABASE quotes_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**Note:** If you want to change the username or password, edit `config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://your_username:your_password@localhost:3306/quotes_db'
```

### 3. Install Python Packages

**From the project directory:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 4. Populate Database

```bash
python init_db.py
```

**This will:**
- Create tables
- Scrape ~900 quotes from quotable.io (9 categories × 100 quotes)
- Take 1-2 minutes

**Expected output:**
```
Creating database tables...
Scraping quotes from sources...
Added Life category with 100 quotes
Added Wisdom category with 100 quotes
...
✅ Database populated successfully!
Total categories: 9
Total quotes: 900
```

### 5. Run the App

```bash
python run.py
```

**Output:**
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 6. Open in Browser

Visit: **http://localhost:5000**

## You're Done! 🎉

### What You Can Do Now

✅ Browse 9 categories of quotes
✅ Search across all quotes
✅ Copy quotes to clipboard
✅ Share quotes
✅ View random quote of the day
✅ Use API endpoints

## Troubleshooting

### Error: "No module named 'pymysql'"
```bash
pip install PyMySQL
```

### Error: "Access denied for user 'root'"
Edit `config.py` and update credentials:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:your_password@localhost:3306/quotes_db'
```

### Error: "Can't connect to MySQL server"
```bash
# Check if MySQL is running
# Windows: Check Services
# macOS: brew services list
# Linux: sudo systemctl status mysql
```

### Error: "Address already in use"
Change port in `run.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)
```

### Scraping takes too long
- Internet connection issue
- quotable.io API temporarily down
- Run again - it will resume

## File Overview

| File | Purpose |
|------|---------|
| `run.py` | Start the app here |
| `config.py` | Database credentials |
| `init_db.py` | Populate database |
| `app/models.py` | Database structure |
| `app/scraper.py` | Quote scraping logic |
| `app/main/routes.py` | Pages and API |
| `app/static/css/style.css` | Styling |
| `app/templates/*.html` | Pages |

## Next Steps

### To Add More Categories
1. Edit `app/scraper.py` - add new method
2. Edit `init_db.py` - add to categories
3. Run `python init_db.py` again

### To Change Colors
Edit `app/static/css/style.css` - update `:root` variables

### To Deploy
1. Change `debug=False` in `run.py`
2. Use production server (Gunicorn, uWSGI)
3. Set `SECRET_KEY` environment variable
4. Update MySQL connection to production server

## API Quick Reference

```bash
# Get random quote
curl http://localhost:5000/api/quotes/random

# Search quotes
curl "http://localhost:5000/api/search?q=success"

# Get category quotes
curl "http://localhost:5000/api/category/life/quotes?page=1"
```

## Questions?

1. Check README.md for detailed info
2. Review error messages in terminal
3. Check browser console (F12) for JavaScript errors
4. Look at database with: `mysql -u root -p quotes_db`

Enjoy! 🌟
