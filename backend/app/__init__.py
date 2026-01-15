import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_object='config.Config'):
    # Setup paths for templates and static files
    basedir = os.path.abspath(os.path.dirname(__file__))
    # Point to frontend templates directory
    template_dir = os.path.abspath(os.path.join(basedir, '..', '..', 'frontend', 'templates', 'templates'))
    static_dir = os.path.abspath(os.path.join(basedir, '..', '..', 'frontend', 'templates', 'templates', 'static'))
    
    app = Flask(
        __name__, 
        template_folder=template_dir,
        static_folder=static_dir,
        static_url_path='/static'
    )
    app.config.from_object(config_object)

    # Enable CORS for all routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)

    # import models
    from .models import Category, Quote

    # register blueprints
    from .main import main as main_bp
    app.register_blueprint(main_bp)

    return app
