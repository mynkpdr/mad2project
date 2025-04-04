from flask_jwt_extended import get_jwt_identity
from flask_restx import Resource
from app.models import Admin, Role, User, Quiz, TakeQuiz, Score, QuizMode, Chapter,Subject
from app.api.api_models.admin import admin_ns
from app.extensions import db, cache
from app.utils.timezone import IndiaNow, IndiaTimeStampNow
from sqlalchemy import func
from datetime import timedelta
from app.decorators import admin_required
from flask import request
from werkzeug.exceptions import NotFound, Conflict
from datetime import datetime
from app.utils.custom import validate_fields
from app.api.api_models.admin import get_admins_model, adminDashboardModel

@admin_ns.route("")
class AdminToken(Resource):
    @admin_ns.marshal_with(get_admins_model)
    @admin_required
    def get(self):
        """Get all admins"""
        admins = Admin.query.all()
        adminsList = [
            {
                "id": admin.user.id,
                "name": admin.user.name,
                "email": admin.user.email,
                "username": admin.user.username,
                "status": admin.user.status.value,
                "email_verified": admin.user.email_verified,
                "date_created": admin.user.date_created,
            }
            for admin in admins
        ]
        return {"data": adminsList}, 200


@admin_ns.route("/dashboard")
@admin_ns.param(
    "quiz_mode", 
    "Quiz mode type", 
    type="string", 
    enum=[mode.value.lower() for mode in QuizMode],
    default=QuizMode.EXAM.value.lower(),
)
@admin_ns.param("days_ago", "Number of days ago to fetch data for", type="integer", default=7)
class AdminDashboardResource(Resource):
    @admin_required
    @admin_ns.marshal_with(adminDashboardModel)
    @cache.cached(timeout=60, query_string=True, key_prefix="admin_dashboard")
    def get(self):
        """Get the admin dashboard data"""
        quiz_mode = request.args.get("quiz_mode", "exam")
        days_ago = int(request.args.get("days_ago", 7))  # Default to 7 days

        # Calculate timestamps
        now = IndiaNow()
        start_date = now - timedelta(days=days_ago)
        start_timestamp = int(start_date.timestamp())

        # Number of active students
        active_students = User.query.filter(
            User.role == Role.STUDENT, User.last_login >= start_timestamp
        ).count()

        # Number of quizzes completed
        quizzes_completed = (
            TakeQuiz.query.filter(
                TakeQuiz.date_created >= start_timestamp,
                TakeQuiz.completed == True,
                Quiz.quiz_mode == QuizMode[quiz_mode.upper()],
            )
            .join(Quiz, Quiz.id == TakeQuiz.quiz_id)
            .count()
        )

        # Query to get the distribution of quizzes based on their difficulty levels (Easy, Medium, Hard and Unset)
        difficulty_level_data = (
            db.session.query(
                Quiz.difficulty_level.label("difficulty_level"),
                func.count(Quiz.id).label("total_quizzes"),
            )
            .filter(Quiz.quiz_mode == QuizMode[quiz_mode.upper()])
            .group_by(Quiz.difficulty_level)
            .all()
        )
        difficulty_level_data = [
            {
                "difficulty_level": data.difficulty_level.value,
                "total_quizzes": data.total_quizzes,
            }
            for data in difficulty_level_data
        ]
        difficulty_level_distribution = {
            "labels": [data["difficulty_level"] for data in difficulty_level_data],
            "data": [data["total_quizzes"] for data in difficulty_level_data],
        }
        total_quizzes = Quiz.query.filter(Quiz.quiz_mode == QuizMode[quiz_mode.upper()]).count()
        total_students = User.query.filter(User.role == Role.STUDENT, User.date_created >= start_timestamp).count()
        response = {
            "total_students": total_students,
            "total_quizzes": total_quizzes,
            "active_students": active_students,
            "quizzes_completed": quizzes_completed,
            "difficulty_level_distribution": difficulty_level_distribution,
        }
        return response, 200


@admin_ns.route("/dashboard/growth-history")
@admin_ns.param(
    "growth_type", 
    "Growth type", 
    type="string", 
    enum=['students', 'take_quizzes'],
    default='students',
)
@admin_ns.param(
    "quiz_mode", 
    "Quiz mode type", 
    type="string", 
    enum=[mode.value.lower() for mode in QuizMode],
    default=QuizMode.EXAM.value.lower(),
)
@admin_ns.param("days_ago", "Number of days ago to fetch data for", type="integer", default=7)
class AdminDashboardGrowthHistoryResource(Resource):
    @admin_required
    @cache.cached(timeout=60, query_string=True, key_prefix="admin_growth_history")
    def get(self):
        """Get points history for charts"""
        growth_type = request.args.get("growth_type", "students")
        days_ago = int(request.args.get("days_ago", 7))  # Default to 7 days
        quiz_mode = request.args.get("quiz_mode", "exam")

        now = IndiaTimeStampNow()
        labels = []
        points = []

        # Calculate intervals based on days_ago
        if days_ago == 1:  # Today - 2 hour gaps
            gap = 2 * 60 * 60  # 2 hours
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

        if growth_type == "students":
            for i in range(intervals):
                end = now - (i * gap)
                start = end - gap

                interval_points = User.query.filter(
                    User.role == Role.STUDENT,
                    User.date_created.between(start, end),
                ).count()
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
        elif growth_type == "take_quizzes":
            for i in range(intervals):
                end = now - (i * gap)
                start = end - gap
                interval_points = (
                    TakeQuiz.query.join(Quiz)
                    .filter(
                        TakeQuiz.date_created.between(start, end),
                        TakeQuiz.completed == True,
                        Quiz.quiz_mode == QuizMode[quiz_mode.upper()],
                    )
                    .count()
                )

                # Format labels based on interval
                if days_ago == 1:
                    label = datetime.fromtimestamp(start).strftime("%I %p")
                elif days_ago == 7:
                    label = datetime.fromtimestamp(start).strftime("%a")
                elif days_ago in [30, 90]:
                    label = datetime.fromtimestamp(start).strftime("%b %d")
                elif days_ago == 180:
                    label = datetime.fromtimestamp(start).strftime("%B")
                else:
                    label = datetime.fromtimestamp(start).strftime("%b-%Y")
                labels.insert(0, label)
                points.insert(0, interval_points)

        return {"labels": labels, "points": points}, 200


@admin_ns.route("/dashboard/charts")
@admin_ns.param(
    "chart_type", 
    "Chart type", 
    type="string", 
    enum=['difficulty_levels', 'subject_avg_scores', 'top_quizzes_by_attempts'],
    default='difficulty_levels',
)
@admin_ns.param(
    "quiz_mode", 
    "Quiz mode type", 
    type="string", 
    enum=[mode.value.lower() for mode in QuizMode],
    default=QuizMode.EXAM.value.lower(),
)
@admin_ns.param("days_ago", "Number of days ago to fetch data for", type="integer", default=7)
@admin_ns.param("direction", "Direction of sorting", type="string", enum=["asc", "desc"], default="desc")
class AdminDashboardChartsResource(Resource):
    @admin_required
    @cache.cached(timeout=60, query_string=True, key_prefix="admin_charts")
    def get(self):
        """Get the data for the charts"""
        chart_type = request.args.get("chart_type", "difficulty_levels")
        quiz_mode = request.args.get("quiz_mode", "exam")
        days_ago = int(request.args.get("days_ago", 7))  # Default to 7 days
        direction = request.args.get("direction", "desc")
        # Calculate timestamps
        now = IndiaNow()
        start_date = now - timedelta(days=days_ago)
        start_timestamp = int(start_date.timestamp())

        if chart_type == "difficulty_levels":
            difficulty_level_data = (
                db.session.query(
                    Quiz.difficulty_level.label("difficulty_level"),
                    func.count(Quiz.id).label("total_quizzes"),
                )
                .filter(Quiz.quiz_mode == QuizMode[quiz_mode.upper()])
                .group_by(Quiz.difficulty_level)
                .all()
            )
            difficulty_level_data = [
                {
                    "difficulty_level": data.difficulty_level.value,
                    "total_quizzes": data.total_quizzes,
                }
                for data in difficulty_level_data
            ]
            difficulty_level_distribution = {
                "labels": [data["difficulty_level"] for data in difficulty_level_data],
                "data": [data["total_quizzes"] for data in difficulty_level_data],
            }
            return difficulty_level_distribution, 200

        elif chart_type == "subject_avg_scores":
            # Get scores where results are available
            scores = (
                Score.query.join(Quiz)
                .join(Chapter)
                .filter(
                    Score.date_created >= start_timestamp,
                    Quiz.quiz_mode == QuizMode[quiz_mode.upper()],
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

        elif chart_type == "top_quizzes_by_attempts":
            top_quizzes = (
                db.session.query(Quiz.name, func.count(TakeQuiz.id).label("attempts_count"))
                .join(TakeQuiz, TakeQuiz.quiz_id == Quiz.id)
                .filter(Quiz.quiz_mode == QuizMode[quiz_mode.upper()])
                .filter(TakeQuiz.date_created >= start_timestamp)
                .group_by(Quiz.id)
                .order_by(func.count(TakeQuiz.id).desc())
                .limit(3)
                .all()
            )
            response = {
                "labels": [q[0] for q in top_quizzes],
                "data": [q[1] for q in top_quizzes],
            }
            return response, 200

@admin_ns.route("/profile")
class AdminProfile(Resource):
    @admin_required
    def get(self):
        """Get the admin profile"""
        user = User.query.get(get_jwt_identity())
        if not user:
            raise NotFound("Admin's profile not found")
        user_data = {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "phone_number": user.phone_number,
            "address": user.address,
            "role": user.role.value,
            "gender": user.gender,
            "dob": user.dob if user.dob else None,
            "profile_picture": user.profile_picture,
            "date_created": (user.date_created if user.date_created else None),
            "last_login": (user.last_login if user.last_login else None),
            "status": user.status.value,
            "bio": user.bio,
            "email_verified": user.email_verified,
        }
        return (user_data), 200


    @admin_required
    def put(self):
        """Update the admin profile"""
        user = User.query.get(get_jwt_identity())
        data = admin_ns.payload
        name = data.get("name", user.name)
        phone_number = data.get("phone_number", user.phone_number)
        address = data.get("address", user.address)
        gender = data.get("gender", user.gender)
        profile_picture = data.get("profile_picture", user.profile_picture)
        bio = data.get("bio", user.bio)
        username = data.get("username", user.username)
        dob = data.get("dob")
        validate_fields(
            [
                ("name", name, True),
                ("username", username, True),
                ("phone_number", phone_number, False),
                ("address", address, False),
                ("gender", gender, False),
                ("dob", dob, False),
                ("profile_picture", profile_picture, False),
                ("bio", bio, False),
            ]
        )
        if (
            User.query.filter_by(username=username).first()
            and username != user.username
        ):
            raise Conflict("Username already exists")

        dob = (
            int(datetime.strptime(dob, "%Y-%m-%d").timestamp() + 60 * 60 * 12)
            if dob
            else None
        )

        user.username = username
        user.name = name
        user.phone_number = phone_number
        user.address = address
        user.gender = gender
        user.profile_picture = profile_picture
        user.bio = bio
        user.dob = dob
        db.session.commit()
        return {"Success": True}, 200
