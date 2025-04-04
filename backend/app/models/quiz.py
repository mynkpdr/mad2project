from app.extensions import db
from enum import Enum
from app.utils.timezone import IndiaTimeStampNow
class DifficultyLevel(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    UNSET = "Unset"

class QuizMode(Enum):
    PRACTICE = "Practice"
    EXAM = "Exam"
# Quiz Table
class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id', ondelete='CASCADE'), nullable=False)
    date_of_quiz = db.Column(db.Integer, default=lambda:IndiaTimeStampNow())
    difficulty_level = db.Column(db.Enum(DifficultyLevel), default=DifficultyLevel.UNSET)
    time_duration = db.Column(db.Integer, nullable=False) #In Seconds
    quiz_mode = db.Column(db.Enum(QuizMode), nullable=False, default=QuizMode.PRACTICE)
    date_created = db.Column(db.Integer, default=lambda:IndiaTimeStampNow())
    description = db.Column(db.String(255), nullable=True)

    chapter = db.relationship('Chapter', back_populates='quizzes')
    scores = db.relationship('Score', back_populates='quiz')
    take_quizzes = db.relationship("TakeQuiz", back_populates="quiz", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Quiz {self.id}>"
    
class TakeQuiz(db.Model):
    __tablename__ = 'take_quiz'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    date_created = db.Column(db.Integer, default=lambda:IndiaTimeStampNow())

    student = db.relationship("Student", back_populates="take_quizzes")
    quiz = db.relationship("Quiz", back_populates="take_quizzes")
    scores = db.relationship("Score", back_populates="take_quiz", cascade="all, delete-orphan")

    quiz_states = db.relationship("QuizState", back_populates="take_quiz")
    def __repr__(self):
        return f"<TakeQuiz id={self.id} quiz_id={self.quiz_id} student_id={self.student_id}>"

class QuizState(db.Model):
    __tablename__ = 'quiz_states'
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    state = db.Column(db.JSON, nullable=False)  # JSON column
    take_quiz_id = db.Column(db.Integer, db.ForeignKey('take_quiz.id', ondelete='CASCADE'), nullable=False)
    result_state = db.Column(db.JSON)
    date_created = db.Column(db.Integer, default=lambda:IndiaTimeStampNow())
    
    take_quiz = db.relationship("TakeQuiz", back_populates="quiz_states")
