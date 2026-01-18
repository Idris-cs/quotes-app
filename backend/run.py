import os
from app import create_app
from config import config

# Get configuration from environment, default to development
env = os.environ.get('FLASK_ENV', 'development')
config_class = config.get(env, config['default'])

app = create_app(config_object=config_class)

if __name__ == '__main__':
    # In production, use a WSGI server (gunicorn, etc.) instead of the development server
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=debug, host='0.0.0.0', port=port)
