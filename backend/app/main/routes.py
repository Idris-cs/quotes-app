from flask import render_template, jsonify, request, abort
from app.main import main
from app import db
from app.models import Category, Quote

@main.route('/')
def index():
    """Home page - display all categories"""
    categories = Category.query.all()
    return render_template('index.html', categories=categories)

@main.route('/category/<slug>')
def category(slug):
    """Display quotes for a specific category"""
    category = Category.query.filter_by(slug=slug).first_or_404()
    quotes = Quote.query.filter_by(category_id=category.id).all()
    return render_template('category.html', category=category, quotes=quotes)

@main.route('/api/quotes/random')
def random_quote():
    """Get a random quote"""
    from sqlalchemy import func
    quote = Quote.query.order_by(func.random()).first()
    if quote:
        return jsonify({
            'id': quote.id,
            'text': quote.text,
            'author': quote.author,
            'category': quote.category.name
        })
    return jsonify({'error': 'No quotes found'}), 404

@main.route('/api/category/<slug>/quotes')
def get_category_quotes(slug):
    """Get quotes for a category via API"""
    category = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    quotes = Quote.query.filter_by(category_id=category.id).paginate(
        page=page, per_page=per_page
    )
    
    return jsonify({
        'category': category.name,
        'total': quotes.total,
        'pages': quotes.pages,
        'current_page': page,
        'quotes': [
            {
                'id': q.id,
                'text': q.text,
                'author': q.author
            }
            for q in quotes.items
        ]
    })

@main.route('/api/search')
def search():
    """Search quotes"""
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify({
            'query': query,
            'error': 'Query must be at least 2 characters',
            'quotes': []
        }), 400
    
    try:
        quotes = Quote.query.filter(
            Quote.text.ilike(f'%{query}%')
        ).limit(20).all()
        
        return jsonify({
            'query': query,
            'count': len(quotes),
            'quotes': [
                {
                    'id': q.id,
                    'text': q.text,
                    'author': q.author,
                    'category': q.category.name
                }
                for q in quotes
            ]
        })
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({
            'query': query,
            'error': 'Search failed',
            'quotes': []
        }), 500
