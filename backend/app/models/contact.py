from app.extensions import db
from app.utils.timezone import IndiaTimeStampNow

# Contact Model
class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=False, nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.Integer, default=lambda:IndiaTimeStampNow())