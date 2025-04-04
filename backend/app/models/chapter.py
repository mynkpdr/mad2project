from app.extensions import db

from app.utils.timezone import IndiaTimeStampNow
# Chapter Table
class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    date_created = db.Column(db.Integer, default=lambda:IndiaTimeStampNow())

    subject = db.relationship('Subject', back_populates='chapters')
    questions = db.relationship("Question", back_populates='chapter', cascade='all, delete-orphan')
    quizzes = db.relationship('Quiz', back_populates='chapter', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Chapter {self.name}>"