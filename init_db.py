import os
import sys
from app import create_app, db
from app.models import Category, Quote
from app.scraper import QuoteScraper

def init_db():
    """Initialize database with quotes"""
    app = create_app()
    
    with app.app_context():
        # Create tables
        print("Creating database tables...")
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
        
        # Add categories and quotes
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
                quote_count=len(quotes_list)
            )
            db.session.add(category)
            db.session.flush()  # Flush to get the category ID
            
            # Add quotes for this category
            for quote_data in quotes_list:
                quote = Quote(
                    text=quote_data['text'],
                    author=quote_data.get('author', 'Unknown'),
                    category_id=category.id,
                    source=quote_data.get('source')
                )
                db.session.add(quote)
            
            print(f"Added {category_name} category with {len(quotes_list)} quotes")
        
        # Commit all changes
        db.session.commit()
        print("\n✅ Database populated successfully!")
        print(f"Total categories: {Category.query.count()}")
        print(f"Total quotes: {Quote.query.count()}")

if __name__ == '__main__':
    init_db()
