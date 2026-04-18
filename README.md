# 📚 Quotes App

A full-stack web application for discovering, browsing, and sharing inspiring quotes across various categories. Built with Flask (backend) and vanilla JavaScript (frontend), featuring Supabase PostgreSQL integration and Docker deployment.

## ✨ Features

- **Quote Categories**: Browse quotes organized by themes (motivation, success, wisdom, etc.)
- **Search Functionality**: Search quotes by keywords
- **Quote of the Day**: Random featured quote refresh
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **RESTful API**: Clean API endpoints for quote management
- **Database Integration**: Supabase PostgreSQL with Flask-SQLAlchemy ORM
- **Docker Support**: Containerized deployment for easy hosting
- **Environment Configuration**: Support for development, testing, and production environments

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 3.1.2
- **ORM**: SQLAlchemy 2.0
- **Database**: PostgreSQL (Supabase support) / SQLite
- **CORS**: Flask-CORS for cross-origin requests
- **Server**: Gunicorn for production

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Responsive styling with animations
- **JavaScript**: Vanilla JS for dynamic interactions
- **Icons**: Font Awesome for UI icons

### Deployment
- **Docker**: Containerized application
- **Render**: Cloud hosting (configured)
- **Environment Variables**: .env configuration

## 📁 Project Structure

```
quotes-app/
├── backend/                          # Flask backend
│   ├── app/
│   │   ├── __init__.py              # Flask app initialization
│   │   ├── main/
│   │   │   ├── routes.py            # Main route handlers
│   │   │   └── __init__.py
│   │   ├── models.py                # SQLAlchemy models
│   │   └── api/                     # API endpoints
│   ├── config.py                    # Configuration classes
│   ├── requirements.txt             # Python dependencies
│   ├── main.py                      # Application entry point
│   ├── run.py                       # Development server
│   └── wsgi.py                      # WSGI entry for production
│
├── frontend/                         # Frontend assets
│   ├── templates/
│   │   ├── base.html               # Base template
│   │   ├── index.html              # Homepage
│   │   └── ...                     # Other templates
│   └── static/
│       ├── css/                    # Stylesheets
│       └── js/                     # JavaScript files
│
├── docker-compose.yml              # Docker Compose configuration
├── Dockerfile                      # Docker build file
├── .env.example                    # Environment template
├── render.yaml                     # Render deployment config
└── README.md                       # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL (or Supabase account) / SQLite
- Git
- Docker (optional)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd quotes-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and other settings
   ```

5. **Initialize database**
   ```bash
   python init_db.py
   ```

6. **Run the development server**
   ```bash
   python run.py
   ```

   The app will be available at `http://localhost:5000`

### Using Docker

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - Open `http://localhost:5000` in your browser

## 📖 API Endpoints

### Quotes
- `GET /api/quotes` - Get all quotes with pagination
- `GET /api/quotes/random` - Get a random quote
- `GET /api/quotes/search?q=keyword` - Search quotes
- `GET /api/quotes/category/<slug>` - Get quotes by category

### Categories
- `GET /api/categories` - List all categories
- `GET /api/categories/<slug>` - Get quotes in a category

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database Configuration
DATABASE_URL=postgresql+psycopg2://user:password@host:5432/dbname
# Or for SQLite: sqlite:///quotes.db

# Application Settings
DEBUG=True
```

### Database Setup

For production with Supabase PostgreSQL:
1. Create a Supabase project
2. Copy your DATABASE_URL
3. Set it in `.env`
4. Run `python init_db.py` to initialize tables

## 🧪 Testing

Run tests to verify functionality:
```bash
python test_endpoints.py
```

## 📝 Documentation

The project includes extensive documentation:
- `ARCHITECTURE.md` - System architecture and design
- `DEPLOYMENT_GUIDE.md` - Production deployment steps
- `DATABASE_SETUP.md` - Database configuration guide
- `QUICK_START.md` - Quick reference guide
- `PROJECT_SUMMARY.md` - Development history and fixes

## 🌐 Deployment

### Render.com (Recommended)
1. Push repository to GitHub
2. Connect repository to Render
3. Follow the `render.yaml` configuration
4. Set environment variables in Render dashboard
5. Deploy!

See `DEPLOYMENT_GUIDE.md` for detailed deployment instructions.

## 🐛 Troubleshooting

### Database Connection Issues
- Verify `DATABASE_URL` is correct in `.env`
- Ensure PostgreSQL is running (if local)
- Check Supabase credentials (if using cloud)

### API Returns 404
- Ensure Flask backend is running on the correct port
- Check that routes are properly configured in `backend/app/main/routes.py`

### Frontend Not Loading Quotes
- Open browser DevTools (F12) and check Console for errors
- Verify API endpoints are accessible
- Check CORS configuration in backend

See detailed guides for more help.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Created by IDrissa Kargbo

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests.

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the author.

---

**Happy Quoting! 🎉**
