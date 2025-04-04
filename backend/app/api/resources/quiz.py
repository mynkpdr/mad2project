from datetime import datetime
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource
import pytz
from app.extensions import db
from app.models import Quiz, QuizMode, QuizState, TakeQuiz, Chapter, User
from app.api.api_models.quiz import quiz_ns, create_quiz_model
from app.utils.custom import validate_fields
from werkzeug.exceptions import NotFound, BadRequest
from app.utils.timezone import IndiaTimeStampNow
from app.decorators import admin_required


@quiz_ns.route("")
class QuizResource(Resource):
    @quiz_ns.expect(create_quiz_model)
    @admin_required
    def post(self):
        """Create a quiz"""
        # Extract payload
        payload = quiz_ns.payload
        name = payload.get("name")
        chapter_id = payload.get("chapter_id")
        difficulty_level = payload.get("difficulty_level")
        date_of_quiz = payload.get("date_of_quiz")
        time_duration = payload.get("time_duration")
        description = payload.get("description")
        quiz_mode = payload.get("quiz_mode")
        validate_fields(
            [
                ("name", name, True),
                ("chapter_id", chapter_id, True),
                ("difficulty_level", difficulty_level, True),
                ("date_of_quiz", date_of_quiz, True),
                ("time_duration", time_duration, True),
                ("description", description, True),
                ("quiz_mode", quiz_mode, True),
            ]
        )
        date_of_quiz = pytz.timezone("Asia/Kolkata").localize(datetime.fromisoformat(date_of_quiz)).timestamp()
        new_quiz = Quiz(
            name=name,
            chapter_id=chapter_id,
            date_of_quiz=date_of_quiz,
            difficulty_level=difficulty_level.upper(),
            time_duration=time_duration * 60,  # Into Seconds
            description=description,
            quiz_mode=QuizMode[quiz_mode.upper()],
        )
        db.session.add(new_quiz)
        db.session.commit()
        return {"success": True}, 201

    @jwt_required()
    def get(self):
        quizzes = Quiz.query.all()
        response = []
        for quiz in quizzes:
            if quiz.date_of_quiz > IndiaTimeStampNow():
                status = "Upcoming"
            elif (
                quiz.date_of_quiz + quiz.time_duration < IndiaTimeStampNow()
                and not quiz.quiz_mode == QuizMode.PRACTICE
            ):
                status = "Completed"
            elif (
                quiz.date_of_quiz
                <= IndiaTimeStampNow()
                <= quiz.date_of_quiz + quiz.time_duration
                and not quiz.quiz_mode == QuizMode.PRACTICE
            ):
                status = "Live"
            elif quiz.quiz_mode == QuizMode.PRACTICE:
                status = "Live"
            response.append(
                {
                    "id": quiz.id,
                    "name": quiz.name,
                    "chapter_id": quiz.chapter_id,
                    "chapter_name": quiz.chapter.name,
                    "total_questions": len(quiz.chapter.questions),
                    "date_of_quiz": quiz.date_of_quiz,
                    "difficulty_level": quiz.difficulty_level.value,
                    "time_duration": quiz.time_duration,
                    "status": status,
                    "quiz_mode": quiz.quiz_mode.value,
                    "date_created": quiz.date_created,
                    "description": quiz.description,
                    "subject_id": quiz.chapter.subject_id,
                    "subject_name": Chapter.query.get(quiz.chapter_id).subject.name,
                }
            )
        return {"data": response}, 200


@quiz_ns.route("/exams")
class QuizExamResource(Resource):
    @jwt_required()
    def get(self):
        user = User.query.get(get_jwt_identity())
        quizzes = Quiz.query.filter(Quiz.quiz_mode == QuizMode.EXAM).all()
        response = []
        for quiz in quizzes:
            status = ""
            attempted = False
            if quiz.date_of_quiz > IndiaTimeStampNow():
                status = "upcoming"
            elif quiz.date_of_quiz + quiz.time_duration < IndiaTimeStampNow():
                status = "expired"
            elif (
                quiz.date_of_quiz
                <= IndiaTimeStampNow()
                <= quiz.date_of_quiz + quiz.time_duration
            ):
                status = "live"
            take_quiz = TakeQuiz.query.filter(
                TakeQuiz.quiz_id == quiz.id, TakeQuiz.student_id == user.student_data.id
            )
            print(take_quiz.all())
            attempted = take_quiz.count() > 0
            completed = take_quiz.filter(TakeQuiz.completed == True).count() > 0
            response.append(
                {
                    "id": quiz.id,
                    "name": quiz.name,
                    "attempted": attempted,
                    "completed": completed,
                    "chapter_id": quiz.chapter_id,
                    "chapter_name": quiz.chapter.name,
                    "total_questions": len(quiz.chapter.questions),
                    "date_of_quiz": quiz.date_of_quiz,
                    "difficulty_level": quiz.difficulty_level.value.lower(),
                    "time_duration": quiz.time_duration,
                    "status": status,
                    "quiz_mode": quiz.quiz_mode.value.lower(),
                    "date_created": quiz.date_created,
                    "description": quiz.description,
                    "subject_id": quiz.chapter.subject_id,
                    "subject_name": Chapter.query.get(quiz.chapter_id).subject.name,
                }
            )
        return {"data": response}, 200


@quiz_ns.route("/practices")
class QuizPracticeResource(Resource):
    @jwt_required()
    def get(self):
        quizzes = Quiz.query.filter(Quiz.quiz_mode == QuizMode.PRACTICE).all()
        response = []
        for quiz in quizzes:
            status = ""
            if quiz.date_of_quiz > IndiaTimeStampNow():
                status = "upcoming"
            else:
                status = "live"
            response.append(
                {
                    "id": quiz.id,
                    "name": quiz.name,
                    "chapter_id": quiz.chapter_id,
                    "chapter_name": quiz.chapter.name,
                    "total_questions": len(quiz.chapter.questions),
                    "date_of_quiz": quiz.date_of_quiz,
                    "difficulty_level": quiz.difficulty_level.value.lower(),
                    "time_duration": quiz.time_duration,
                    "status": status,
                    "quiz_mode": quiz.quiz_mode.value.lower(),
                    "date_created": quiz.date_created,
                    "description": quiz.description,
                    "subject_id": quiz.chapter.subject_id,
                    "subject_name": Chapter.query.get(quiz.chapter_id).subject.name,
                }
            )
        return {"data": response}, 200


@quiz_ns.route("/upcoming")
class QuizUpcomingResource(Resource):
    @jwt_required()
    
    def get(self):
        quiz_mode = request.args.get("quiz_mode")
        quizzes = (
            Quiz.query.filter(
                Quiz.date_of_quiz > IndiaTimeStampNow(),
                Quiz.quiz_mode == QuizMode[quiz_mode.upper()],
            ).all()
            if quiz_mode
            else Quiz.query.filter(Quiz.date_of_quiz > IndiaTimeStampNow()).all()
        )
        response = []
        for quiz in quizzes:
            response.append(
                {
                    "id": quiz.id,
                    "name": quiz.name,
                    "chapter_id": quiz.chapter_id,
                    "chapter_name": quiz.chapter.name,
                    "total_questions": len(quiz.chapter.questions),
                    "date_of_quiz": quiz.date_of_quiz,
                    "difficulty_level": quiz.difficulty_level.value.lower(),
                    "time_duration": quiz.time_duration,
                    "status": "upcoming",
                    "quiz_mode": quiz.quiz_mode.value.lower(),
                    "date_created": quiz.date_created,
                    "description": quiz.description,
                    "subject_id": quiz.chapter.subject_id,
                    "subject_name": Chapter.query.get(quiz.chapter_id).subject.name,
                }
            )
        return {"data": response}, 200


@quiz_ns.route("/<int:quiz_id>")
class SingleQuizResource(Resource):
    @jwt_required()
    def get(self, quiz_id):
        user_role = User.query.get(get_jwt_identity()).role.value
        """Get a quiz by ID"""
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            raise NotFound(f"Quiz with id {quiz_id} not found")
        response = {
            "id": quiz.id,
            "name": quiz.name,
            "chapter_id": quiz.chapter_id,
            "subject_id": Chapter.query.get(quiz.chapter_id).subject_id,
            "total_questions": len(quiz.chapter.questions),
            "date_of_quiz": quiz.date_of_quiz,
            "difficulty_level": quiz.difficulty_level.value,
            "time_duration": quiz.time_duration,
            "quiz_mode": quiz.quiz_mode.value,
            "date_created": quiz.date_created,
            "description": quiz.description,
            "questions": [
                {
                    "id": question.id,
                    "question_statement": question.question_statement,
                    "question_type": question.question_type.value,
                    "marks": question.marks,
                    "date_created": question.date_created,
                }
                for question in quiz.chapter.questions if quiz.date_of_quiz < IndiaTimeStampNow() or user_role.upper() == "ADMIN"
            ],
        }
        return {"data": response}, 200

    @admin_required
    def delete(self, quiz_id):
        """Delete a quiz by ID"""
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            raise NotFound(f"Quiz with id {quiz_id} not found")
        db.session.delete(quiz)
        db.session.commit()
        return {"message": "Quiz deleted successfully"}, 200

    @admin_required
    def put(self, quiz_id):
        """Edit a quiz"""
        # Extract payload
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            raise NotFound(f"Quiz with id {quiz_id} not found")
        payload = quiz_ns.payload
        name = payload.get("name", quiz.name)
        chapter_id = payload.get("chapter_id", quiz.chapter_id)
        difficulty_level = payload.get("difficulty_level", quiz.difficulty_level.value)
        date_of_quiz = payload.get("date_of_quiz", datetime.fromtimestamp(quiz.date_of_quiz).strftime("%Y-%m-%dT%H:%M"))
        time_duration = payload.get("time_duration", quiz.time_duration)
        description = payload.get("description", quiz.description)
        quiz_mode = payload.get("quiz_mode", quiz.quiz_mode.value)
        validate_fields(
            [
                ("name", name, True),
                ("chapter_id", chapter_id, True),
                ("difficulty_level", difficulty_level, True),
                ("date_of_quiz", date_of_quiz, True),
                ("time_duration", time_duration, True),
                ("description", description, True),
                ("quiz_mode", quiz_mode, True),
            ]
        )
        date_of_quiz = pytz.timezone("Asia/Kolkata").localize(datetime.fromisoformat(date_of_quiz)).timestamp()

        quiz.name = name
        quiz.chapter_id = chapter_id
        quiz.difficulty_level = difficulty_level.upper()
        quiz.date_of_quiz = date_of_quiz
        quiz.time_duration = time_duration * 60
        quiz.description = description
        quiz.quiz_mode = QuizMode[quiz_mode.upper()]
        db.session.commit()
        return {"success": True}, 200


@quiz_ns.route("/<int:quiz_id>/questions")
class SingleQuizQuestionsResource(Resource):
    @jwt_required()
    def get(self, quiz_id):
        """Get all questions of a quiz"""
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            raise NotFound(f"Quiz with ID {quiz_id} not found")
        questions = (
            quiz.chapter.questions if quiz.date_of_quiz < IndiaTimeStampNow() else []
        )  # Only show questions if the quiz has started
        response = []

        for index, question in enumerate(questions):
            response.append(
                {
                    "id": question.id,
                    "display_id": index + 1,
                    "question_image": question.question_image,
                    "statement": question.question_statement,
                    "answer_explanation": (
                        question.answer_explanation
                        if quiz.quiz_mode == QuizMode.PRACTICE
                        else None
                    ),
                    "marks": question.marks,
                    "type": question.question_type.value,
                    "date_created": question.date_created,
                    "options": [
                        {
                            "id": option.id,
                            "text": option.option_text,
                            "is_correct": (
                                option.is_correct
                                if quiz.quiz_mode == QuizMode.PRACTICE
                                else None
                            ),
                        }
                        for option in question.options
                    ],
                    "correct_answers": (
                        [ca.answer_text for ca in question.correct_answers]
                        if quiz.quiz_mode == QuizMode.PRACTICE
                        else []
                    ),
                }
            )
        return {
            "data": {
                "questions": response,
                "name": quiz.name,
                "chapter_name": quiz.chapter.name,
                "difficulty_level": quiz.difficulty_level.value,
                "time_duration": quiz.time_duration,
                "quiz_mode": quiz.quiz_mode.value,
            }
        }, 200


@quiz_ns.route("/<int:quiz_id>/take_quiz")
class TakeQuizResource(Resource):
    @jwt_required()
    def post(self, quiz_id):
        """Take a quiz"""
        user = User.query.get(get_jwt_identity())
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            raise NotFound(f"Quiz with ID {quiz_id} not found")

        if quiz.date_of_quiz > IndiaTimeStampNow():
            raise BadRequest("The quiz has not started yet")

        if quiz.quiz_mode == QuizMode.PRACTICE:
            new_take_quiz = TakeQuiz(
                student_id=user.student_data.id,
                quiz_id=quiz_id,
            )
            db.session.add(new_take_quiz)
            db.session.commit()
            return {
                "data": {
                    "take_quiz_id": new_take_quiz.id,
                    "take_quiz_time_remaining": quiz.time_duration,
                    "take_quiz_completed": False,
                    "existing": False,
                    "id": quiz.id,
                    "name": quiz.name,
                    "quiz_mode": quiz.quiz_mode.value,
                    "chapter_name": quiz.chapter.name,
                    "difficulty_level": quiz.difficulty_level.value,
                    "time_duration": quiz.time_duration,
                }
            }, 200

        elif quiz.quiz_mode == QuizMode.EXAM:
            if quiz.date_of_quiz + quiz.time_duration < IndiaTimeStampNow():
                raise BadRequest("The quiz has expired")
            existing_take_quiz = TakeQuiz.query.filter(
                TakeQuiz.student_id == user.student_data.id, TakeQuiz.quiz_id == quiz_id
            ).first()

            if not existing_take_quiz:
                new_take_quiz = TakeQuiz(
                    student_id=user.student_data.id, quiz_id=quiz_id
                )
                db.session.add(new_take_quiz)
                db.session.commit()
                return {
                    "data": {
                        "take_quiz_id": new_take_quiz.id,
                        "take_quiz_time_remaining": quiz.time_duration,
                        "take_quiz_completed": False,
                        "existing": False,
                        "id": quiz.id,
                        "name": quiz.name,
                        "quiz_mode": quiz.quiz_mode.value,
                        "chapter_name": quiz.chapter.name,
                        "difficulty_level": quiz.difficulty_level.value,
                        "time_duration": quiz.time_duration,
                    }
                }, 200

            else:
                end_time = existing_take_quiz.date_created + quiz.time_duration
                remaining_time = end_time - IndiaTimeStampNow()
                time_remaining = max(0, remaining_time)
                return {
                    "data": {
                        "existing_take_quiz_id": existing_take_quiz.id,
                        "existing_take_quiz_time_remaining": time_remaining,
                        "existing_take_quiz_completed": existing_take_quiz.completed,
                        "existing": True,
                        "id": quiz.id,
                        "name": quiz.name,
                        "quiz_mode": quiz.quiz_mode.value,
                        "chapter_name": quiz.chapter.name,
                        "difficulty_level": quiz.difficulty_level.value,
                        "time_duration": quiz.time_duration,
                    }
                }, 200


@quiz_ns.route("/<int:quiz_id>/take_quiz/is_existing")
class IsExistingTakeQuizResource(Resource):
    @jwt_required()
    def post(self, quiz_id):
        """Check if a quiz is already taken by the user"""
        user = User.query.get(get_jwt_identity())
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            raise NotFound(f"Quiz with ID {quiz_id} not found")
        existing_take_quiz = TakeQuiz.query.filter(
            TakeQuiz.student_id == user.student_data.id, TakeQuiz.quiz_id == quiz_id
        ).first()
        if (
            existing_take_quiz
            and quiz.quiz_mode == QuizMode.EXAM
            and existing_take_quiz.completed
        ):
            raise BadRequest("You have already completed this quiz")

        if quiz.date_of_quiz + quiz.time_duration < IndiaTimeStampNow():
            raise BadRequest("The quiz has expired")

        if quiz.date_of_quiz > IndiaTimeStampNow():
            raise BadRequest("The quiz has not started yet")

        total_marks = sum(question.marks for question in quiz.chapter.questions)
        if existing_take_quiz:
            quiz_state = QuizState.query.filter(
                QuizState.take_quiz_id == existing_take_quiz.id
            ).first()
            return {
                "data": {
                    "existing": True,
                    "name": quiz.name,
                    "quiz_state": quiz_state.state if quiz_state else {},
                    "chapter_name": quiz.chapter.name,
                    "difficulty_level": quiz.difficulty_level.value,
                    "time_duration": quiz.time_duration,
                    "quiz_mode": quiz.quiz_mode.value,
                    "completed": existing_take_quiz.completed,
                    "total_marks": total_marks,
                }
            }, 200
        else:
            return {
                "data": {
                    "existing": False,
                    "name": quiz.name,
                    "chapter_name": quiz.chapter.name,
                    "difficulty_level": quiz.difficulty_level.value,
                    "time_duration": quiz.time_duration,
                    "quiz_mode": quiz.quiz_mode.value,
                    "completed": False,
                    "total_marks": total_marks,
                }
            }, 200
