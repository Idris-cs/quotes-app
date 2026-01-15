import os
import time
import argparse
from urllib.parse import urlparse, urlunparse

from app import create_app, db
from app.models import Category, Quote
from app.scraper import QuoteScraper
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

def mask_db_url(url: str) -> str:
    if not url:
        return 'Not set'
    try:
        p = urlparse(url)
        netloc = p.netloc
        if '@' in netloc:
            _, hostpart = netloc.split('@', 1)
            masked_netloc = '***@' + hostpart
        else:
            masked_netloc = netloc
        masked = urlunparse((p.scheme, masked_netloc, p.path or '', '', '', ''))
        return masked
    except Exception:
        return '***masked***'


def init_db():
    """Initialize database with quotes"""
    app = create_app()

    with app.app_context():
        # Create tables (with connection retry for remote DB like Supabase)
        print("Checking database connectivity and creating tables...")

        # Test DB connection with retries
        retries = int(os.environ.get('DB_CONNECT_RETRIES', '5'))
        base_delay = float(os.environ.get('DB_CONNECT_BASE_DELAY', '1.0'))
        connected = False
        for attempt in range(1, retries + 1):
            try:
                db.session.execute(text('SELECT 1'))
                connected = True
                break
            except OperationalError as e:
                delay = base_delay * (2 ** (attempt - 1))
                print(f"Database not ready (attempt {attempt}/{retries}): {e}. Retrying in {delay:.1f}s")
                time.sleep(delay)

        if not connected:
            print("Failed to connect to the database after several attempts. Check DATABASE_URL and network.")
            return

        # Drop existing tables and recreate (ensure schema matches models)
        db.drop_all()
        db.create_all()

        # Check if data already exists
        if Category.query.first():
            print("Database already populated!")
            return

        # Scrape quotes
        print("Scraping quotes from sources...")
        scraper = QuoteScraper()
        all_quotes = scraper.all_quotes()

        # Define categories with metadata
        categories_meta = {
            'Life': {
                'slug': 'life',
                'description': 'Quotes about life, living, and everyday wisdom',
                'icon': '🌟'
            },
            'Wisdom': {
                'slug': 'wisdom',
                'description': 'Timeless wisdom and philosophical insights',
                'icon': '🧠'
            },
            'Motivation': {
                'slug': 'motivation',
                'description': 'Get motivated to achieve your goals',
                'icon': '🚀'
            },
            'Success': {
                'slug': 'success',
                'description': 'Insights on achieving success',
                'icon': '🏆'
            },
            'Friendship': {
                'slug': 'friendship',
                'description': 'Celebrating friendship and bonds',
                'icon': '🤝'
            },
            'Love': {
                'slug': 'love',
                'description': 'Beautiful words about love',
                'icon': '❤️'
            },
            'Inspiration': {
                'slug': 'inspiration',
                'description': 'Find daily inspiration',
                'icon': '✨'
            },
            'Faith': {
                'slug': 'faith',
                'description': 'Spiritual and faith-based quotes',
                'icon': '🙏'
            },
            'Courage': {
                'slug': 'courage',
                'description': 'Embrace courage and strength',
                'icon': '💪'
            }
        }

        # Add categories and quotes (avoid duplicates when re-running against Supabase)
        for category_name, quotes_list in all_quotes.items():
            if not quotes_list:
                print(f"Skipping {category_name} - no quotes found")
                continue

            meta = categories_meta.get(category_name, {})
            category = Category(
                name=category_name,
                slug=meta.get('slug', category_name.lower()),
                description=meta.get('description', ''),
                icon=meta.get('icon', '📖'),
                quote_count=0,
            )
            db.session.add(category)
            db.session.flush()  # Flush to get the category ID

            added = 0
            for quote_data in quotes_list:
                q_text = quote_data.get('text')
                q_author = quote_data.get('author', 'Unknown')
                # Skip duplicates by text + author
                exists = Quote.query.filter_by(text=q_text, author=q_author).first()
                if exists:
                    continue

                tags = quote_data.get('tags') or []
                if isinstance(tags, str):
                    tags_val = tags
                else:
                    tags_val = ','.join(tags) if tags else None

                quote = Quote(
                    text=q_text,
                    author=q_author,
                    tags=tags_val,
                    category_id=category.id,
                    source=quote_data.get('source')
                )
                db.session.add(quote)
                added += 1

            category.quote_count = added
            print(f"Added {category_name} category with {added} quotes")

        # Commit all changes
        db.session.commit()
        print("\n✅ Database populated successfully!")
        print(f"Total categories: {Category.query.count()}")
        print(f"Total quotes: {Quote.query.count()}")


def main():
    parser = argparse.ArgumentParser(description='Initialize database or show DB config')
    parser.add_argument('--show-db', action='store_true', help='Print masked DATABASE_URL and exit')
    args = parser.parse_args()

    if args.show_db:
        app = create_app()
        with app.app_context():
            db_uri = app.config.get('SQLALCHEMY_DATABASE_URI') or os.environ.get('DATABASE_URL')
            print('Resolved DB URI (masked):', mask_db_url(db_uri))
        return

    # Default action: run the DB initializer
    init_db()


if __name__ == '__main__':
    main()
