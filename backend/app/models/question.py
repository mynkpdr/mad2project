
from app.extensions import db
from enum import Enum
from app.utils.timezone import IndiaTimeStampNow
class QuestionType(Enum):
    MCQ = "MCQ"          # Multiple Choice Question
    MSQ = "MSQ"          # Multiple Select Question
    NUMERICAL = "Numerical"  # Numerical Question

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question_statement = db.Column(db.String(255), nullable=False)
    question_image = db.Column(db.String(255), nullable=True)
    question_type = db.Column(db.Enum(QuestionType), nullable=False)
    answer_explanation = db.Column(db.String(255), nullable=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id', ondelete='CASCADE'), nullable=False)
    marks = db.Column(db.Integer, default=1)
    date_created = db.Column(db.Integer, default=lambda:IndiaTimeStampNow())

    correct_answers = db.relationship('CorrectAnswer', back_populates='question', cascade='all, delete-orphan')
    options = db.relationship('Option', back_populates='question', cascade='all, delete-orphan')
    chapter = db.relationship('Chapter', back_populates='questions')
    
    def __repr__(self):
        return f"<Question {self.question_statement}>"

# Option Table
class Option(db.Model):
    __tablename__ = 'options'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    option_text = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

    question = db.relationship('Question', back_populates='options', uselist=False)

    def __repr__(self):
        return f"<Option {self.option_text}>"

# CorrectAnswer Table
class CorrectAnswer(db.Model):
    __tablename__ = 'correct_answers'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('options.id'), nullable=True)
    answer_text = db.Column(db.String(255), nullable=True)

    question = db.relationship('Question', back_populates='correct_answers', uselist=False)
    option = db.relationship('Option')

    def __repr__(self):
        return f"<CorrectAnswer {self.answer_text}>"

