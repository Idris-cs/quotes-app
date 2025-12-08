from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_object='config.Config'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)

    # import models
    from .models import Category, Quote

    # register blueprints
    from .main import main as main_bp
    app.register_blueprint(main_bp)

    return app
