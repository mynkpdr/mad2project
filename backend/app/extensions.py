from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from celery import Celery
import os
db = SQLAlchemy()
migrate = Migrate()
cors = CORS(supports_credentials=True)
mail = Mail()
jwt = JWTManager()
bcrypt = Bcrypt()
cache = Cache()
celery = Celery('tasks', backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0'), broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'), include=['app.tasks'])
