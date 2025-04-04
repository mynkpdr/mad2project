from app import create_app
from app.extensions import celery

app = create_app() # Create the Flask application
app.app_context().push() # Push the application context to create_app() function

celery.conf.update(app.config['CELERY_CONFIG']) 
