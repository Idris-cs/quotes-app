import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

# Load .env from project root (one level above this file) if present,
# otherwise allow load_dotenv() to search from the current working dir.
project_env = os.path.abspath(os.path.join(basedir, os.pardir, '.env'))
if os.path.exists(project_env):
    load_dotenv(project_env)
else:
    load_dotenv()


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-quotes-app-change-in-production')
    
    # Database for persistent storage. Supports Supabase (Postgres) or local SQLite.
    # If using Supabase, set DATABASE_URL (example: postgresql://user:pass@host:5432/dbname)
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        # SQLAlchemy prefers the 'postgresql+psycopg2' scheme
        db_url = db_url.replace('postgres://', 'postgresql+psycopg2://', 1)
        db_url = db_url.replace('postgresql://', 'postgresql+psycopg2://', 1)
    SQLALCHEMY_DATABASE_URI = db_url or 'sqlite:///' + os.path.join(basedir, 'quotes.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = 3600
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True  # Require HTTPS in production


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Select config based on environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
