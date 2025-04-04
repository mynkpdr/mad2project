from dotenv import load_dotenv
import os
from datetime import timedelta
load_dotenv()


class DevelopmentConfig():
    """Development-specific configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", os.urandom(24))
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    ALLOWED_EXTENSIONS_IMAGE = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
    MAX_FILE_SIZE = 1 * 1024 * 1024  # Limit file upload size to 1 MB
    ERROR_404_HELP = False

    CACHE_TYPE = 'SimpleCache'
    # CACHE_TYPE = 'RedisCache'
    # CACHE_REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_DEFAULT_TIMEOUT = 60 # 1 minute

    # Redis & Celery Configuration
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL

    CELERY_CONFIG = {
        'broker_url': REDIS_URL,
        'result_backend': REDIS_URL,
        'broker_connection_retry_on_startup': True,
        'timezone': 'Asia/Kolkata'
    }


class ProductionConfig():
    """Production configuration settings."""
    ENV = 'production'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config_options = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
