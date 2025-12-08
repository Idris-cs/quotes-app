# Quotes App

A professional, fully-featured quotes application with web scraping, MySQL database, and beautiful responsive UI.

## Features

- 🎨 **Professional UI**: Modern, gradient-based design with smooth animations
- 📱 **Fully Responsive**: Works perfectly on desktop, tablet, and mobile
- 💾 **MySQL Database**: Organized storage for quotes by category
- 🔍 **Search Functionality**: Find quotes across all categories
- 🎭 **9 Quote Categories**: Life, Wisdom, Motivation, Success, Friendship, Love, Inspiration, Faith, Courage
- 📊 **100+ Quotes Per Category**: Extensive quote collection
- 🌐 **Copy & Share**: Share quotes directly or copy to clipboard
- ⚡ **Fast Performance**: Optimized queries and caching

## Quote Categories

1. **Life** - Quotes about living and everyday wisdom
2. **Wisdom** - Timeless wisdom and philosophical insights
3. **Motivation** - Get motivated to achieve your goals
4. **Success** - Insights on achieving success
5. **Friendship** - Celebrating friendship and bonds
6. **Love** - Beautiful words about love
7. **Inspiration** - Find daily inspiration
8. **Faith** - Spiritual and faith-based quotes
9. **Courage** - Embrace courage and strength

## Installation

### Prerequisites

- Python 3.8+
- MySQL Server 5.7+
- pip (Python package manager)

### Step 1: Clone or Set Up Project

```bash
cd c:\Users\Idrissa\quotes-app
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure MySQL

1. **Create Database**:

```sql
CREATE DATABASE quotes_db;
CREATE USER 'root'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON quotes_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

2. **Update Configuration** (if needed):

Edit `config.py` and update the MySQL credentials:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost:3306/quotes_db'
```

### Step 5: Initialize Database

```bash
python init_db.py
```

This script will:
- Create database tables
- Scrape 100+ quotes from quotable.io for each category
- Populate the database with all quotes

### Step 6: Run the Application

```bash
python run.py
```

The app will be available at: **http://localhost:5000**

## Usage

### Home Page (`/`)
- View all quote categories in a professional grid layout
- Click any category to browse quotes
- View "Quote of the Day" with a refresh button
- Search across all quotes using the search feature

### Category Page (`/category/<slug>`)
- Browse all quotes for a specific category
- Copy quotes to clipboard with one click
- Share quotes via native sharing (on supported devices)
- View quote author and source information

### Search Feature
- Click "Search Quotes" in navigation
- Type to search across all quotes
- View results with category information
- Quick access to find specific quotes

### API Endpoints

#### Get Random Quote
```
GET /api/quotes/random
```

Response:
```json
{
    "id": 1,
    "text": "Quote text here",
    "author": "Author Name",
    "category": "Life"
}
```

#### Get Category Quotes (Paginated)
```
GET /api/category/<slug>/quotes?page=1&per_page=10
```

#### Search Quotes
```
GET /api/search?q=success
```

Response:
```json
{
    "query": "success",
    "count": 5,
    "quotes": [
        {
            "id": 1,
            "text": "Quote text",
            "author": "Author",
            "category": "Success"
        }
    ]
}
```

## Project Structure

```
quotes-app/
├── app/
│   ├── __init__.py           # Flask app initialization
│   ├── models.py             # Database models
│   ├── scraper.py            # Web scraper
│   ├── main/
│   │   ├── __init__.py
│   │   └── routes.py         # Flask routes
│   ├── static/
│   │   └── css/
│   │       └── style.css     # Professional styling
│   └── templates/
│       ├── base.html         # Base template
│       ├── index.html        # Home page
│       └── category.html     # Category page
├── config.py                 # Configuration
├── run.py                    # Application entry point
├── wsgi.py                   # WSGI server entry
├── init_db.py               # Database initialization script
└── requirements.txt         # Python dependencies
```

## Database Schema

### Categories Table
```sql
CREATE TABLE categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    quote_count INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Quotes Table
```sql
CREATE TABLE quotes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    text TEXT NOT NULL,
    author VARCHAR(255),
    category_id INT NOT NULL,
    source VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);
```

## Technologies Used

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Migrate
- **Database**: MySQL, PyMySQL
- **Web Scraping**: Requests, BeautifulSoup4
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **UI/UX**: Responsive Design, Modern Gradients, Smooth Animations

## Customization

### Add New Quote Category

1. Add method in `app/scraper.py`:

```python
def get_custom_quotes(self):
    """Scrape custom category quotes"""
    quotes = []
    try:
        url = "https://api.quotable.io/quotes?tags=custom&limit=150"
        response = self.session.get(url, headers=self.headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for quote in data.get('results', []):
                quotes.append({
                    'text': quote['content'],
                    'author': quote.get('author', 'Unknown'),
                    'source': 'quotable.io'
                })
    except Exception as e:
        print(f"Error: {e}")
    return quotes[:100]
```

2. Add to `all_quotes()` method
3. Run `python init_db.py` to scrape and populate

### Change Color Scheme

Edit CSS variables in `app/static/css/style.css`:

```css
:root {
    --primary-color: #YOUR_COLOR;
    --secondary-color: #YOUR_COLOR;
    --accent-color: #YOUR_COLOR;
    /* ... */
}
```

## Troubleshooting

### Database Connection Error
- Verify MySQL is running
- Check credentials in `config.py`
- Ensure database `quotes_db` exists

### Scraping Fails
- Check internet connection
- Verify `quotable.io` API is accessible
- Try again - API may be temporarily unavailable

### Port Already in Use
```bash
# Change port in run.py or use:
python run.py --port 5001
```

## Performance Optimization

- Database queries are optimized with proper indexing
- CSS is minified for production
- JavaScript uses vanilla (no jQuery required)
- Images are not used - only text and emojis for faster loading

## Security Notes

- Use strong MySQL passwords in production
- Set `SECRET_KEY` environment variable
- Use HTTPS in production
- Validate and sanitize user inputs

## Future Enhancements

- User accounts and favorites
- Quote ratings and comments
- Category management admin panel
- Email daily quote feature
- Mobile app version
- API rate limiting
- Advanced caching

## License

This project is open source and available for personal and commercial use.

## Support

For issues or questions:
1. Check troubleshooting section
2. Review database logs
3. Check browser console for JavaScript errors

## Credits

- Quotes sourced from [quotable.io](https://quotable.io)
- Built with Flask and modern web technologies