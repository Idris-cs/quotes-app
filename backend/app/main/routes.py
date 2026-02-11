from flask import render_template, jsonify, request, abort, session
from app.main import main
from app import db
from app.models import Category, Quote, Favourite
import uuid

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

def get_session_id():
    """Get or create a session ID for the user"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session.modified = True  # Ensure session is saved
    return session['session_id']

@main.route('/api/favourites', methods=['GET'])
def get_favourites():
    """Get all favourite quotes for the user"""
    session_id = get_session_id()
    print(f"Getting favourites for session: {session_id}")
    
    try:
        favourites = db.session.query(Quote).join(
            Favourite, Quote.id == Favourite.quote_id
        ).filter(Favourite.session_id == session_id).all()
        
        print(f"Found {len(favourites)} favourites")
        return jsonify({
            'count': len(favourites),
            'quotes': [
                {
                    'id': q.id,
                    'text': q.text,
                    'author': q.author,
                    'category': q.category.name
                }
                for q in favourites
            ]
        })
    except Exception as e:
        print(f"Favourites error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to retrieve favourites', 'details': str(e)}), 500

@main.route('/api/favourites/<int:quote_id>', methods=['POST'])
def add_favourite(quote_id):
    """Add a quote to favourites"""
    session_id = get_session_id()
    print(f"Adding favourite: quote_id={quote_id}, session_id={session_id}")
    
    try:
        quote = Quote.query.get_or_404(quote_id)
        
        # Check if already favourited
        existing = Favourite.query.filter_by(
            quote_id=quote_id, 
            session_id=session_id
        ).first()
        
        if existing:
            print(f"Quote {quote_id} already in favourites")
            return jsonify({'message': 'Quote already in favourites'}), 200
        
        favourite = Favourite(quote_id=quote_id, session_id=session_id)
        db.session.add(favourite)
        db.session.commit()
        
        print(f"Successfully added quote {quote_id} to favourites")
        return jsonify({
            'message': 'Quote added to favourites',
            'quote': {
                'id': quote.id,
                'text': quote.text,
                'author': quote.author
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"Add favourite error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to add favourite', 'details': str(e)}), 500

@main.route('/api/favourites/<int:quote_id>', methods=['DELETE'])
def remove_favourite(quote_id):
    """Remove a quote from favourites"""
    session_id = get_session_id()
    print(f"Removing favourite: quote_id={quote_id}, session_id={session_id}")
    
    try:
        favourite = Favourite.query.filter_by(
            quote_id=quote_id, 
            session_id=session_id
        ).first_or_404()
        
        db.session.delete(favourite)
        db.session.commit()
        
        print(f"Successfully removed quote {quote_id} from favourites")
        return jsonify({'message': 'Quote removed from favourites'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Remove favourite error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to remove favourite', 'details': str(e)}), 500

@main.route('/api/favourites/<int:quote_id>/check', methods=['GET'])
def check_favourite(quote_id):
    """Check if a quote is in user's favourites"""
    session_id = get_session_id()
    print(f"Checking favourite: quote_id={quote_id}, session_id={session_id}")
    
    try:
        is_favourite = Favourite.query.filter_by(
            quote_id=quote_id,
            session_id=session_id
        ).first() is not None
        
        print(f"Quote {quote_id} favourite status: {is_favourite}")
        return jsonify({'is_favourite': is_favourite}), 200
    except Exception as e:
        print(f"Check favourite error: {e}")
        return jsonify({'error': 'Failed to check favourite'}), 500

@main.route('/favourites')
def favourites():
    """Display user's favourite quotes"""
    return render_template('favourites.html')
