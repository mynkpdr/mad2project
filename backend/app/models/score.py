from app.extensions import db
from app.utils.timezone import IndiaTimeStampNow
from app.models.quiz import QuizMode, QuizState

# Score Table
class Score(db.Model):
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(
        db.Integer, db.ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False
    )
    student_id = db.Column(
        db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    date_created = db.Column(db.Integer, default=lambda: IndiaTimeStampNow())
    total_scored = db.Column(db.Integer, nullable=False)  # Percentage
    time_taken = db.Column(db.Integer, nullable=False)  # In Seconds
    take_quiz_id = db.Column(
        db.Integer, db.ForeignKey("take_quiz.id", ondelete="CASCADE")
    )
    quiz = db.relationship("Quiz", back_populates="scores")
    student = db.relationship("Student", back_populates="scores")
    take_quiz = db.relationship("TakeQuiz", back_populates="scores")

    def __repr__(self):
        return f"<Score {self.student_id} - {self.total_scored}>"

    @property
    def display_result(self):
        time_taken = self.time_taken
        quiz_state = QuizState.query.filter_by(take_quiz_id=self.take_quiz_id).first()
        state = quiz_state.state
        if not state:
            return None
        if self.quiz.quiz_mode == QuizMode.EXAM and IndiaTimeStampNow() > self.quiz.date_of_quiz + (
            self.quiz.time_duration * 2
        ):  # If the quiz is an exam and the current time is greater than the quiz time * 2 times the quiz duration
            total_scored = self.total_scored
            result_state = quiz_state.result_state
            total_questions = len(result_state["data"]["questions"])
            return {
                "total_scored": total_scored,
                "time_taken": time_taken,
                "state": state,
                "result_state": result_state,
                "total_questions": total_questions,
            }
        elif self.quiz.quiz_mode == QuizMode.PRACTICE:
            total_scored = self.total_scored
            result_state = quiz_state.result_state
            total_questions = len(result_state["data"]["questions"])
            return {
                "total_scored": total_scored,
                "time_taken": time_taken,
                "state": state,
                "result_state": result_state,
                "total_questions": total_questions,
            }
        else:
            return None

    @property
    def is_result_available(self):
        if (self.quiz.quiz_mode == QuizMode.EXAM and IndiaTimeStampNow() > self.quiz.date_of_quiz + (
            self.quiz.time_duration * 2
        ) or self.quiz.quiz_mode == QuizMode.PRACTICE):
            return True
        return False