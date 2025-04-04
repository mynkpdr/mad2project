from app.api.api_models.take_quiz import take_quiz_ns
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload
from app.models import Question, QuestionType, Quiz, TakeQuiz, QuizMode, QuizState, User, Score
from app.extensions import db
from werkzeug.exceptions import NotFound, Conflict, Forbidden
from app.utils.timezone import IndiaTimeStampNow


@take_quiz_ns.route("/<int:take_quiz_id>/submit")
class SubmitQuizResource(Resource):
    @jwt_required()
    def post(self, take_quiz_id):
        """Submit a quiz"""
        user = User.query.get(get_jwt_identity())
        take_quiz = TakeQuiz.query.get(take_quiz_id)
        quiz = Quiz.query.get(take_quiz.quiz_id)

        if not take_quiz:
            raise NotFound(f"Take Quiz with ID {take_quiz_id} not found")
        if take_quiz.student_id != user.student_data.id:
            raise Forbidden("You are not allowed to access this")
        if quiz.quiz_mode == QuizMode.EXAM and take_quiz.completed:
            raise Conflict("The quiz has already been submitted")

        formatted_questions = []
        total_marks = sum(question.marks for question in quiz.chapter.questions)
        total_marks_scored = 0
        time_taken = int((IndiaTimeStampNow() - take_quiz.date_created))

        quiz_state = take_quiz_ns.payload.get("quiz_state")
        for index, (question_id, question_data) in enumerate(quiz_state.items()):
            question = (
                Question.query.options(
                    joinedload(Question.options), joinedload(Question.correct_answers)
                )
                .filter_by(id=int(question_id))
                .first()
            )

            # Calculate score
            question_score = 0
            selected_values = question_data.get("selected_values", [])
            if not isinstance(selected_values, list):
                selected_values = (
                    [selected_values] if selected_values is not None else []
                )
            # Get correct answers
            correct_answer_ids = (
                [ca.option_id for ca in question.correct_answers]
                if question.question_type in [QuestionType.MCQ, QuestionType.MSQ]
                else [str(ca.answer_text) for ca in question.correct_answers]
            )

            # Score calculation based on question type
            if selected_values:
                if question.question_type == QuestionType.MCQ:
                    if selected_values and selected_values[0] in correct_answer_ids:
                        question_score = question.marks
                elif question.question_type == QuestionType.MSQ:
                    selected_set = set(selected_values)
                    correct_set = set(correct_answer_ids)
                    if selected_set == correct_set:
                        question_score = question.marks
                    elif selected_set.issubset(correct_set):
                        question_score = round(
                            (question.marks * len(selected_set)) / len(correct_set), 2
                        )
                elif question.question_type == QuestionType.NUMERICAL:
                    correct_answer_ids = [str(question.correct_answers[0].answer_text)]
                    if str(selected_values[0]) == str(
                        question.correct_answers[0].answer_text
                    ):
                        question_score = question.marks

                total_marks_scored += question_score

            # Format question data
            formatted_question = {
                "id": question.id,
                "display_id": index + 1,
                "total_marks": question.marks,
                "answer_explanation": question.answer_explanation,
                "statement": question.question_statement,
                "type": question.question_type.value,
                "score": question_score,
                "question_image": question.question_image,
                "options": (
                    [
                        {"id": opt.id, "text": opt.option_text}
                        for opt in question.options
                    ]
                    if question.question_type in [QuestionType.MCQ, QuestionType.MSQ]
                    else None
                ),
                "selected_answer": selected_values,
                "correct_answer": correct_answer_ids,
            }
            formatted_questions.append(formatted_question)

        # Save score and update quiz state
        total_scored = round((total_marks_scored / total_marks * 100), 2)
        new_score = Score(
            student_id=user.student_data.id,
            quiz_id=quiz.id,
            total_scored=total_scored,
            time_taken=time_taken,
            take_quiz_id=take_quiz_id,
        )
        db.session.add(new_score)
        take_quiz.completed = True
        db.session.commit()

        # Update quiz state
        existing_quiz_state = QuizState.query.filter(
            QuizState.take_quiz_id == take_quiz_id
        ).first()
        result_state = {
            "data": {
                "score": {
                    "scored": round(total_marks_scored, 2),
                    "total": total_marks,
                    "percentage": total_scored,
                    "timeTaken": time_taken,
                },
                "questions": formatted_questions,
            }
        }
        if existing_quiz_state:
            existing_quiz_state.state = quiz_state
            existing_quiz_state.result_state = result_state
            db.session.commit()
        else:
            new_quiz_state = QuizState(
                take_quiz_id=take_quiz_id, state=quiz_state, result_state=result_state
            )
            db.session.add(new_quiz_state)
            db.session.commit()

        if quiz.quiz_mode == QuizMode.EXAM:
            return {"success": True}, 200
        elif quiz.quiz_mode == QuizMode.PRACTICE:
            return result_state, 200


@take_quiz_ns.route("/<int:take_quiz_id>/save")
class SaveQuizResource(Resource):
    @jwt_required()
    def post(self, take_quiz_id):
        """Save a quiz state"""
        quiz_state = take_quiz_ns.payload["quiz_state"]
        existing_quiz_state = QuizState.query.filter(
            QuizState.take_quiz_id == take_quiz_id
        ).first()
        if existing_quiz_state:
            existing_quiz_state.state = quiz_state
            db.session.commit()
            return {"success": True}, 200
        else:
            new_quiz_state = QuizState(take_quiz_id=take_quiz_id, state=quiz_state)
            db.session.add(new_quiz_state)
            db.session.commit()
            return {"success": True}, 200
