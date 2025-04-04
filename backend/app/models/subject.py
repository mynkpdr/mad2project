from app.extensions import db
from app.utils.timezone import IndiaTimeStampNow

# Subject Table
class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    date_created = db.Column(db.Integer, default=lambda:IndiaTimeStampNow())

    chapters = db.relationship('Chapter', back_populates='subject', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Subject {self.name}>"