#!/usr/bin/env python
"""
Admin CLI for managing quotes and categories
"""

import click
from app import create_app, db
from app.models import Category, Quote
from app.scraper import QuoteScraper

app = create_app()

@click.group()
def cli():
    """Quotes App Administration"""
    pass

@cli.command()
def init_db():
    """Initialize database with sample data"""
    with app.app_context():
        click.echo("Creating database tables...")
        db.create_all()
        
        if Category.query.first():
            click.echo("Database already contains data!")
            return
        
        click.echo("Scraping quotes from sources...")
        scraper = QuoteScraper()
        all_quotes = scraper.all_quotes()
        
        categories_meta = {
            'Life': {'slug': 'life', 'description': 'Quotes about life and everyday wisdom', 'icon': '🌟'},
            'Wisdom': {'slug': 'wisdom', 'description': 'Timeless wisdom and insights', 'icon': '🧠'},
            'Motivation': {'slug': 'motivation', 'description': 'Motivational quotes', 'icon': '🚀'},
            'Success': {'slug': 'success', 'description': 'Success and achievement quotes', 'icon': '🏆'},
            'Friendship': {'slug': 'friendship', 'description': 'Friendship quotes', 'icon': '🤝'},
            'Love': {'slug': 'love', 'description': 'Love and relationships', 'icon': '❤️'},
            'Inspiration': {'slug': 'inspiration', 'description': 'Daily inspiration', 'icon': '✨'},
            'Faith': {'slug': 'faith', 'description': 'Spiritual and faith quotes', 'icon': '🙏'},
            'Courage': {'slug': 'courage', 'description': 'Courage and strength', 'icon': '💪'},
        }
        
        for category_name, quotes_list in all_quotes.items():
            if not quotes_list:
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
            db.session.flush()
            
            for quote_data in quotes_list:
                quote = Quote(
                    text=quote_data['text'],
                    author=quote_data.get('author', 'Unknown'),
                    category_id=category.id,
                    source=quote_data.get('source', 'Web')
                )
                db.session.add(quote)
            
            click.echo(f"✓ {category_name}: {len(quotes_list)} quotes")
        
        db.session.commit()
        click.echo(f"\n✅ Database initialized!")
        click.echo(f"   Categories: {Category.query.count()}")
        click.echo(f"   Quotes: {Quote.query.count()}")

@cli.command()
@click.option('--category', default=None, help='Category name')
def count_quotes(category):
    """Count quotes in database"""
    with app.app_context():
        if category:
            cat = Category.query.filter_by(name=category).first()
            if cat:
                count = Quote.query.filter_by(category_id=cat.id).count()
                click.echo(f"{category}: {count} quotes")
            else:
                click.echo(f"Category '{category}' not found")
        else:
            categories = Category.query.all()
            total = 0
            for cat in categories:
                count = Quote.query.filter_by(category_id=cat.id).count()
                click.echo(f"{cat.name}: {count} quotes")
                total += count
            click.echo(f"\nTotal: {total} quotes")

@cli.command()
def list_categories():
    """List all categories"""
    with app.app_context():
        categories = Category.query.all()
        if not categories:
            click.echo("No categories found")
            return
        
        click.echo("\nAvailable Categories:")
        click.echo("-" * 50)
        for cat in categories:
            quote_count = Quote.query.filter_by(category_id=cat.id).count()
            click.echo(f"{cat.icon} {cat.name:<15} ({quote_count} quotes)")

@cli.command()
@click.option('--category', prompt='Category name', help='Name of category')
@click.option('--slug', prompt='Category slug', help='URL-friendly name')
@click.option('--description', prompt='Description', help='Category description')
@click.option('--icon', default='📖', help='Category icon/emoji')
def add_category(category, slug, description, icon):
    """Add a new category"""
    with app.app_context():
        if Category.query.filter_by(slug=slug).first():
            click.echo("Category slug already exists")
            return
        
        cat = Category(
            name=category,
            slug=slug,
            description=description,
            icon=icon
        )
        db.session.add(cat)
        db.session.commit()
        click.echo(f"✓ Category '{category}' added")

@cli.command()
@click.option('--category', prompt='Category slug', help='Category slug')
@click.option('--text', prompt='Quote text', help='Quote text')
@click.option('--author', prompt='Author', help='Quote author')
def add_quote(category, text, author):
    """Add a quote manually"""
    with app.app_context():
        cat = Category.query.filter_by(slug=category).first()
        if not cat:
            click.echo(f"Category '{category}' not found")
            return
        
        quote = Quote(
            text=text,
            author=author,
            category_id=cat.id,
            source='Manual'
        )
        db.session.add(quote)
        db.session.commit()
        click.echo(f"✓ Quote added to {cat.name}")

@cli.command()
def clear_data():
    """Clear all data from database"""
    if click.confirm("This will delete all quotes and categories. Continue?"):
        with app.app_context():
            Quote.query.delete()
            Category.query.delete()
            db.session.commit()
            click.echo("✓ Database cleared")

@cli.command()
@click.option('--limit', default=5, help='Number of quotes to show')
def sample_quotes(limit):
    """Show sample quotes"""
    with app.app_context():
        quotes = Quote.query.limit(limit).all()
        if not quotes:
            click.echo("No quotes found")
            return
        
        for i, quote in enumerate(quotes, 1):
            click.echo(f"\n{i}. \"{quote.text}\"")
            click.echo(f"   — {quote.author}")
            click.echo(f"   Category: {quote.category.name}")

@cli.command()
def check_health():
    """Check database health"""
    with app.app_context():
        try:
            categories = Category.query.count()
            quotes = Quote.query.count()
            
            click.echo("Database Health Check")
            click.echo("-" * 30)
            click.echo(f"✓ Database connection: OK")
            click.echo(f"✓ Categories: {categories}")
            click.echo(f"✓ Quotes: {quotes}")
            
            if categories == 0 or quotes == 0:
                click.echo("\n⚠️  No data found. Run: python admin.py init-db")
            else:
                click.echo("\n✅ Everything looks good!")
        except Exception as e:
            click.echo(f"❌ Error: {e}")

if __name__ == '__main__':
    cli()
