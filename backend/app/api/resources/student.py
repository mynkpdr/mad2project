from datetime import datetime, timedelta
from flask import request
from flask_restx import Resource
from app.models import (
    Role,
    Student,
    User,
    Quiz,
    QuizMode,
    TakeQuiz,
    Score,
    Chapter,
    Subject
)
from app.extensions import db, cache
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.api_models.student import student_ns, get_student_model, get_students_model
from werkzeug.exceptions import NotFound, Conflict, Forbidden

from app.decorators import admin_required
from app.utils.custom import calculate_points, validate_fields
from app.utils.timezone import IndiaNow, IndiaTimeStampNow


# Student API Resource
@student_ns.route("")
class StudentResource(Resource):
    @admin_required
    @student_ns.marshal_with(get_students_model)
    def get(self):
        """Get all students"""
        students = Student.query.all()
        student_data = [
            {
                "id": student.id,
                "username": student.user.username,
                "name": student.user.name,
                "email": student.user.email,
                "phone_number": student.user.phone_number,
                "address": student.user.address,
                "role": student.user.role.value,
                "gender": student.user.gender,
                "dob": student.user.dob if student.user.dob else None,
                "profile_picture": student.user.profile_picture,
                "date_created": (
                    student.user.date_created if student.user.date_created else None
                ),
                "qualification": student.qualification,
                "last_login": (
                    student.user.last_login if student.user.last_login else None
                ),
                "status": student.user.status.value,
                "bio": student.user.bio,
                "email_verified": student.user.email_verified,
            }
            for student in students
        ]
        return {"data": student_data}, 200


@student_ns.route("/<int:student_id>")
class SingleStudentResource(Resource):
    @jwt_required()
    @student_ns.marshal_with(get_student_model)
    def get(self, student_id):
        """Get a student"""
        user = User.query.get(get_jwt_identity())
        if user and user.role == Role.ADMIN:
            student = Student.query.get(student_id)
        else:
            student = User.query.get(get_jwt_identity()).student_data
        if not student:
            raise NotFound(f"Student with id {student_id} not found")
        if not student.id == int(student_id):
            raise Forbidden("You are not authorized to perform this action")
        student_data = {
            "id": student.id,
            "username": student.user.username,
            "name": student.user.name,
            "email": student.user.email,
            "phone_number": student.user.phone_number,
            "address": student.user.address,
            "role": student.user.role.value,
            "gender": student.user.gender,
            "dob": student.user.dob if student.user.dob else None,
            "profile_picture": student.user.profile_picture,
            "date_created": (
                student.user.date_created if student.user.date_created else None
            ),
            "qualification": student.qualification,
            "last_login": (
                student.user.last_login if student.user.last_login else None
            ),
            "status": student.user.status.value,
            "bio": student.user.bio,
            "email_verified": student.user.email_verified,
        }
        return {"data": student_data}, 200

    @jwt_required()
    def put(self, student_id):
        """Update the student profile"""
        user = User.query.get(get_jwt_identity())
        if user and user.role == Role.ADMIN:
            student = Student.query.get(student_id)
        else:
            student = User.query.get(get_jwt_identity()).student_data
        if not student:
            raise NotFound(f"Student with id {student_id} not found")
        if not student.id == int(student_id):
            raise Forbidden("You are not authorized to perform this action")
        data = student_ns.payload
        name = data.get("name", student.user.name)
        email = data.get("email", student.user.email)
        phone_number = data.get("phone_number", student.user.phone_number)
        address = data.get("address", student.user.address)
        gender = data.get("gender", student.user.gender)
        profile_picture = data.get("profile_picture", student.user.profile_picture)
        bio = data.get("bio", student.user.bio)
        status = data.get("status", student.user.status.value)
        qualification = data.get("qualification", student.qualification)
        username = data.get("username", student.user.username)
        dob = data.get("dob")
        validate_fields(
            [
                ("name", name, True),
                ("email", email, True),
                ("username", username, True),
                ("phone_number", phone_number, False),
                ("address", address, False),
                ("gender", gender, False),
                ("dob", dob, False),
                ("status", status, False),
                ("profile_picture", profile_picture, False),
                ("bio", bio, False),
                ("qualification", qualification, False),
            ]
        )
        if (
            User.query.filter_by(username=username).first()
            and username != student.user.username
        ):
            raise Conflict("Username already exists")
        if User.query.filter_by(email=email).first() and email != student.user.email:
            raise Conflict("Email already exists")

        dob = (
            int(datetime.strptime(dob, "%Y-%m-%d").timestamp() + 60 * 60 * 12)
            if dob
            else None
        )

        student.user.username = username
        student.user.name = name
        student.user.email = email
        student.user.phone_number = phone_number
        student.user.address = address
        student.user.gender = gender
        student.user.profile_picture = profile_picture
        student.user.bio = bio
        if user.role == Role.ADMIN:
            student.user.status = status.upper()
        student.user.dob = dob
        student.qualification = qualification
        db.session.commit()
        return {"Success": True}, 200

    @admin_required
    def delete(self, student_id):
        """Delete a student"""
        student = Student.query.get(student_id)
        if not student:
            raise NotFound(f"Student with id {student_id} not found")
        user = User.query.get(student.user_id)

        db.session.delete(user)
        db.session.commit()
        return {"Success": True}, 200


@student_ns.route("/leaderboard")
class StudentsLeaderboardResource(Resource):
    @jwt_required()
    def get(self):
        """Get all students leaderboard"""
        days_ago = int(request.args.get("days_ago", 7))
        quiz_mode = request.args.get("quiz_mode", "exam").upper()

        # Calculate timestamps
        now = IndiaNow()
        start_date = now - timedelta(days=days_ago)
        start_timestamp = int(start_date.timestamp())

        # Get all students first
        students = Student.query.all()
        leaderboard = []

        # Calculate stats for each student
        for student in students:
            # Get completed quizzes for this student
            scores = (
                Score.query.join(Quiz)
                .filter(
                    Score.student_id == student.id,
                    Score.date_created >= start_timestamp,
                    Quiz.quiz_mode == QuizMode[quiz_mode.upper()],
                )
                .all()
            )
            scores = [score for score in scores if score.is_result_available]
            avg_score = 0
            avg_time = 0
            if scores:  # Only include students who have taken quizzes
                avg_score = int(
                    sum(s.total_scored for s in scores)
                    / len(scores)
                )
                avg_time = float(
                    sum(s.time_taken for s in scores)
                    / len(scores)
                )

            total_quizzes = len(scores)
            points_earned = calculate_points(avg_score, avg_time, total_quizzes)
            leaderboard.append(
                {
                    "student_id": student.id,
                    "name": student.user.name,
                    "username": student.user.username,
                    "points_earned": points_earned,
                    "total_quizzes": total_quizzes,
                    "profile_picture": student.user.profile_picture,
                }
            )

        # Sort leaderboard by points
        leaderboard.sort(key=lambda x: x["points_earned"], reverse=True)

        return {"data": leaderboard}


@student_ns.route("/dashboard")
class StudentDashboardResource(Resource):
    @jwt_required()
    @cache.cached(timeout=60, query_string=True, key_prefix="student_dashboard")
    def get(self):
        """Get the student dashboard"""
        user = User.query.get(get_jwt_identity())
        if user.role == Role.ADMIN:
            student_id = request.args.get("student_id")
            validate_fields([("student_id", student_id, True)])
            user = Student.query.get(student_id).user
        days_ago = int(request.args.get("days_ago", 7))
        quiz_mode = request.args.get("quiz_mode", "exam").upper()

        # Calculate timestamps
        now = IndiaNow()
        start_date = now - timedelta(days=days_ago)
        start_timestamp = int(start_date.timestamp())

        # Get average score and time taken
        scores = (
            Score.query.join(Quiz)
            .filter(
                Score.student_id == user.student_data.id,
                Score.date_created >= start_timestamp,
                Quiz.quiz_mode == QuizMode[quiz_mode.upper()],
            )
            .all()
        )
        pending_result = any(not score.is_result_available for score in scores)
        completed_quizzes = sum(
            1 for score in scores if TakeQuiz.query.get(score.take_quiz_id).completed
        )
        scores = [score for score in scores if score.is_result_available]
        avg_score = 0
        avg_time = 0
        if scores:
            avg_score = int(
                sum(s.total_scored for s in scores)
                / len(scores)
            )
            avg_time = float(
                sum(s.time_taken for s in scores) / len(scores)
            )

        total_quizzes = len(scores)

        points_earned = calculate_points(avg_score, avg_time, total_quizzes)
        
        response_data = {
            "total_quizzes": total_quizzes,
            "avg_score": avg_score,
            "completed_quizzes": completed_quizzes,
            "points_earned": points_earned,
            "pending_result": pending_result,
            "avg_time": avg_time,
        }

        return response_data, 200


@student_ns.route("/dashboard/points_history")
class StudentPointsHistoryResource(Resource):
    @cache.cached(timeout=60, query_string=True, key_prefix="points_history")
    @jwt_required()
    def get(self):
        """Get points history for charts"""
        user = User.query.get(get_jwt_identity())
        if user and user.role == Role.ADMIN:
            student_id = request.args.get("student_id")
            validate_fields([("student_id", student_id, True)])
            user = Student.query.get(student_id).user
        days_ago = int(request.args.get("days_ago", 7))  # Default to 7 days
        quiz_mode = request.args.get("quiz_mode", "exam")

        now = IndiaTimeStampNow()
        labels = []
        points = []

        # Calculate intervals based on days_ago
        if days_ago == 1:  # Today - 4 hour gaps
            gap = 2 * 60 * 60  # 1 hours
            intervals = 12
        elif days_ago == 7:  # Week - daily gaps
            gap = 24 * 60 * 60  # 1 day
            intervals = 7
        elif days_ago == 30:  # Month - 5 day gaps
            gap = 5 * 24 * 60 * 60  # 5 days
            intervals = 6
        elif days_ago == 90:  # 3 months - 15 day gaps
            gap = 15 * 24 * 60 * 60  # 15 days
            intervals = 6
        elif days_ago == 180:  # 6 months - monthly gaps
            gap = 30 * 24 * 60 * 60  # 30 days
            intervals = 6
        elif days_ago == 365:  # Year - 2 month gaps
            gap = 60 * 24 * 60 * 60  # 60 days
            intervals = 6

        for i in range(intervals):
            end = now - (i * gap)
            start = end - gap

            # Get all scores up to this interval's end time
            scores = (
                Score.query.join(Quiz)
                .filter(
                    Score.student_id == user.student_data.id,
                    Score.date_created <= end,
                    Quiz.quiz_mode == QuizMode[quiz_mode.upper()],
                )
                .all()
            )

            # Calculate cumulative points up to this interval
            interval_points = 0
            if scores:
                avg_score = int(
                    sum(
                        s.total_scored
                        for s in scores
                        if s.is_result_available
                    )
                    / len(scores)
                )
                avg_time = float(
                    sum(
                        s.time_taken
                        for s in scores
                        if s.is_result_available
                    )
                    / len(scores)
                )
                total_quizzes = sum(
                    1 for score in scores if score.is_result_available
                )

                interval_points = calculate_points(avg_score, avg_time, total_quizzes)

            # Format labels based on interval
            if days_ago == 1:
                label = datetime.fromtimestamp(start).strftime("%I %p")
            elif days_ago == 7:
                label = datetime.fromtimestamp(start).strftime("%a")
            elif days_ago in [30, 90]:
                label = datetime.fromtimestamp(start).strftime("%b %d")
            elif days_ago == 180:
                label = datetime.fromtimestamp(start).strftime("%B")
            else:  # year
                label = datetime.fromtimestamp(start).strftime("%b-%Y")

            labels.insert(0, label)
            points.insert(0, interval_points)

        return {"labels": labels, "points": points}, 200


@student_ns.route("/dashboard/charts")
class StudentChartsResource(Resource):
    @jwt_required()
    @cache.cached(timeout=60, query_string=True, key_prefix="student_charts")
    def get(self):
        """Get student's subject-wise performance charts"""
        user = User.query.get(get_jwt_identity())
        if user and user.role == Role.ADMIN:
            student_id = request.args.get("student_id")
            validate_fields([("student_id", student_id, True)])
            user = Student.query.get(student_id).user
        days_ago = int(request.args.get("days_ago", 7))  # Default to 7 days
        quiz_mode = request.args.get("quiz_mode", "exam").upper()
        direction = request.args.get("direction", "desc")

        # Calculate timestamps
        now = IndiaNow()
        start_date = now - timedelta(days=days_ago)
        start_timestamp = int(start_date.timestamp())

        # Get scores where results are available
        scores = (
            Score.query.join(Quiz)
            .join(Chapter)
            .filter(
                Score.student_id == user.student_data.id,
                Score.date_created >= start_timestamp,
                Quiz.quiz_mode == QuizMode[quiz_mode],
            )
            .all()
        )

        # Group scores by subject and calculate averages
        subject_scores = {}
        for score in scores:
            if score.is_result_available:  # Only include available results
                subject_id = Quiz.query.get(score.quiz_id).chapter.subject_id
                if subject_id not in subject_scores:
                    subject_scores[subject_id] = []
                subject_scores[subject_id].append(score.total_scored)

        # Calculate averages and prepare data
        subject_avg_scores = []
        for subject_id, scores_list in subject_scores.items():
            if scores_list:  # Only include if there are scores
                avg_score = sum(scores_list) / len(scores_list)
                subject_avg_scores.append((subject_id, avg_score))

        # Sort based on direction
        subject_avg_scores.sort(key=lambda x: x[1], reverse=(direction != "asc"))
        subject_avg_scores = subject_avg_scores[:5]  # Limit to top/bottom 5

        # Format the response
        subject_scores_data = {"labels": [], "data": []}
        for subject_id, avg_score in subject_avg_scores:
            subject = Subject.query.get(subject_id)
            if subject:
                subject_scores_data["labels"].append(subject.name)
                subject_scores_data["data"].append(round(float(avg_score), 2))

        return subject_scores_data, 200


@student_ns.route("/dashboard/time-score")
class StudentTimeScoreResource(Resource):
    @jwt_required()
    @cache.cached(timeout=60, query_string=True, key_prefix="time_score")
    def get(self):
        """Get time vs score data for scatter plot"""

        user = User.query.get(get_jwt_identity())
        if user and user.role == Role.ADMIN:
            student_id = request.args.get("student_id")
            validate_fields([("student_id", student_id, True)])
            user = Student.query.get(student_id).user
        days_ago = int(request.args.get("days_ago", 7))
        quiz_mode = request.args.get("quiz_mode", "exam").upper()

        # Calculate timestamps
        now = IndiaNow()
        start_date = now - timedelta(days=days_ago)
        start_timestamp = int(start_date.timestamp())

        # Get score data with time taken
        scores = (
            Score.query.join(Quiz)
            .filter(
                Score.student_id == user.student_data.id,
                Score.date_created >= start_timestamp,
                Quiz.quiz_mode == QuizMode[quiz_mode],
            )
            .all()
        )

        # Format data for scatter plot
        scatter_data = [
            {
                "time": score.time_taken / 60,
                "time_taken": score.time_taken,
                "score": score.total_scored,
                "quiz_name": Quiz.query.get(score.quiz_id).name,
            }
            for score in scores
            if score.is_result_available
        ]

        return scatter_data, 200


@student_ns.route("/take_quizzes")
class StudentQuizzesResource(Resource):
    @jwt_required()
    def get(self):
        """Get all quizzes taken by the student"""
        user = User.query.get(get_jwt_identity())
        if user and user.role == Role.ADMIN:
            student_id = request.args.get("student_id")
            validate_fields([("student_id", student_id, True)])
            user = Student.query.get(student_id).user
        days_ago = request.args.get("days_ago", None)
        if days_ago:
            days_ago = int(days_ago)
            now = IndiaNow()
            start_date = now - timedelta(days=days_ago)
            start_timestamp = int(start_date.timestamp())
            take_quizzes = TakeQuiz.query.filter(
                TakeQuiz.student_id == user.student_data.id,
                TakeQuiz.date_created >= start_timestamp,
            ).all()
        else:
            take_quizzes = TakeQuiz.query.filter(
                TakeQuiz.student_id == user.student_data.id
            ).all()

        quizzes = []
        if take_quizzes:
            quizzes = []
            for take_quiz in take_quizzes:
                quiz = Quiz.query.get(take_quiz.quiz_id)
                score = Score.query.filter_by(take_quiz_id=take_quiz.id).first()
                if take_quiz.completed and score:
                    pending_result = not score.is_result_available
                    total_scored = None
                    if score.is_result_available:
                        total_scored = score.display_result["total_scored"]
                else:
                    pending_result = False
                    total_scored = None
                quizzes.append(
                    {
                        "quiz_id": quiz.id,
                        "quiz_name": quiz.name,
                        "quiz_mode": quiz.quiz_mode.value.lower(),
                        "total_scored": total_scored,
                        "take_quiz_id": take_quiz.id,
                        "pending_result": pending_result,
                        "completed": take_quiz.completed,
                        "date_taken": take_quiz.date_created,
                    }
                )
        return {"data": quizzes}, 200


@student_ns.route("/take_quizzes/<int:take_quizzes_id>")
class StudentQuizResource(Resource):
    @jwt_required()
    def get(self, take_quizzes_id):
        """Get the quiz taken by the student"""
        user = User.query.get(get_jwt_identity())
        take_quiz = TakeQuiz.query.get(take_quizzes_id)
        if user and user.role == Role.ADMIN:
            user = Student.query.get(take_quiz.student_id).user
        if not take_quiz:
            raise NotFound(f"Data not found")
        if take_quiz.student_id != user.student_data.id:
            raise Forbidden("You are not authorized to view this data")
        quiz = Quiz.query.get(take_quiz.quiz_id)
        score = Score.query.filter_by(take_quiz_id=take_quiz.id).first()

        # Get others average
        others_scores = (
            Score.query.join(Quiz)
            .filter(
                Score.quiz_id == quiz.id,
                Score.student_id != user.student_data.id,  # Not the same student
            )
            .all()
        )
        others_average = 0
        if others_scores:
            others_average = sum(
                s.total_scored for s in others_scores if s.is_result_available
            ) / len(
                others_scores
            )  # Average of others

        total_scored, time_taken, state, result_state, total_questions = (
            None,
            None,
            {},
            {},
            None,
        )

        if score and score.is_result_available:
            total_scored, time_taken, state, result_state, total_questions = (
                score.display_result["total_scored"],
                score.display_result["time_taken"],
                score.display_result["state"],
                score.display_result["result_state"],
                score.display_result["total_questions"],
            )

        quiz_data = {
            "student_name": user.name,
            "student_profile_picture": user.profile_picture,
            "quiz_id": quiz.id,
            "quiz_name": quiz.name,
            "quiz_mode": quiz.quiz_mode.value.lower(),
            "quiz_difficulty": quiz.difficulty_level.value.lower(),
            "total_questions": total_questions,
            "total_scored_percentage": total_scored,
            "total_percentage": 100,
            "total_scored_marks": (
                result_state["data"]["score"]["scored"] if result_state else None
            ),
            "total_marks": (
                result_state["data"]["score"]["total"] if result_state else None
            ),
            "time_taken": time_taken,
            "total_time": quiz.time_duration,
            "take_quiz_id": take_quiz.id,
            "result_state": result_state,
            "state": state,
            "completed": take_quiz.completed,
            "date_taken": take_quiz.date_created,
            "others_average": round(others_average, 2),
        }
        return {"data": quiz_data}, 200
