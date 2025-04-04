import os
from flask import json, render_template
from flask_jwt_extended import create_access_token
from app.extensions import celery
from app.utils.export import send_email_with_attachment
from app.utils.send_email import send_email
from app.models.user import Status, Student, User, Role
from celery.schedules import crontab
from app.utils.timezone import IndiaNow, IndiaTimeStampNow
from datetime import datetime, timedelta
from urllib.parse import urlencode
import csv
import tempfile
from app.models.quiz import Quiz
from flask import current_app
from app.api.resources.student import (
    StudentDashboardResource,
    StudentPointsHistoryResource,
    StudentChartsResource,
    StudentTimeScoreResource,
    StudentQuizzesResource,
)


# WORKERS
@celery.task(name="tasks.send_email_with_attachment")
def send_email_with_attachment_async(to, subject, body, html_body, file_path, filename):
    """Send an email with an attachment asynchronously"""
    send_email_with_attachment(to, subject, body, html_body, file_path, filename)
    return {"message": "Email sent successfully"}


@celery.task(name="tasks.send_email")
def send_email_async(to, subject, body, html_body):
    """Send an email asynchronously"""
    send_email(to, subject, body, html_body)
    return {"message": "Email sent successfully"}


# SCHEDULED TASKS
@celery.task(name="tasks.send_reminder_emails")
def send_reminder_email():
    """Send reminder emails to user"""
    new_quizzes = Quiz.query.filter(Quiz.date_of_quiz > IndiaTimeStampNow()).limit(5).all()
    if new_quizzes:
        for user in User.query.filter(
            User.role == Role.STUDENT,
            User.email_verified == True,
            User.status == Status.ACTIVE,
            User.notifications == True
        ).all():
            for quiz in new_quizzes:
                quiz.date_of_quiz = datetime.fromtimestamp(quiz.date_of_quiz).strftime(
                    "%B %d, %Y %I:%M %p"
                )
            send_email(
                to=user.email,
                subject="New Quiz Reminder",
                body=f"You have {len(new_quizzes)} new quizzes available",
                html_body=render_template(
                    "reminder_email.html",
                    user=user,
                    new_quizzes=new_quizzes,
                    frontend_url=os.getenv("FRONTEND_URL"),
                ),
            )
        return {"message": "Reminder emails sent successfully"}


@celery.task(name="tasks.send_activity_report")
def send_activity_report(frequency, selected_quiz_mode):
    """Send activity report to all users"""

    admin_user = User.query.filter(User.role == Role.ADMIN).first()
    jwt_token = create_access_token(identity=str(admin_user.id))

    student_dashboard = {
        "avg_score": None,
        "completed_quizzes": None,
        "points_earned": None,
        "pending_result": False,
    }
    students = Student.query.join(User).filter(User.status == Status.ACTIVE).with_entities(Student.id, User.email).all()
    for student in students:
        student_id = student.id
        with current_app.app_context():
            with current_app.test_request_context(
                headers={"Authorization": f"Bearer {jwt_token}"},
                query_string={
                    "student_id": student_id,
                    "quiz_mode": selected_quiz_mode,
                    "days_ago": (30 if frequency == "monthly" else 7),
                },
            ):
                from app.extensions import cache
                cache.clear()
                student_dashboard, code = StudentDashboardResource().get()
                cache.clear()
                student_points_history, code = StudentPointsHistoryResource().get()
                cache.clear()
                student_charts, code = StudentChartsResource().get()
                cache.clear()
                student_time_score, code = StudentTimeScoreResource().get()
                cache.clear()
                student_quizzes, code = StudentQuizzesResource().get()

            with current_app.test_request_context(
                headers={"Authorization": f"Bearer {jwt_token}"},
                query_string={
                    "student_id": student_id,
                    "quiz_mode": "practice" if selected_quiz_mode == "exam" else "exam",
                    "days_ago": (30 if frequency == "monthly" else 7),
                },
            ):
                student_points_history_2, code = StudentPointsHistoryResource().get()

        # Generate the chart data
        student_comparision_config = {
            "type": "line",
            "data": {
                "labels": student_points_history["labels"],
                "datasets": [
                    {
                        "label": f"{'Exam' if selected_quiz_mode == 'exam' else 'Practice'} Points",
                        "data": student_points_history["points"],
                        "borderColor": "#046A38",
                        "backgroundColor": "rgba(4, 106, 56, 0.1)",
                        "fill": True,
                        "lineTension": 0.4,
                    },
                    {
                        "label": f"{'Practice' if selected_quiz_mode == 'exam' else 'Exam'} Points",
                        "data": student_points_history_2["points"],
                        "borderColor": "#FFC107",
                        "backgroundColor": "rgba(255, 193, 7, 0.1)",
                        "fill": True,
                        "lineTension": 0.4,
                    },
                ],
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "scales": {
                    "yAxes": [
                        {
                            "scaleLabel": {
                                "display": True,
                                "labelString": "Points",
                            },
                        },
                    ],
                    "xAxes": [
                        {
                            "scaleLabel": {
                                "display": True,
                                "labelString": "Days",
                            },
                        },
                    ],
                },
            },
        }

        student_time_score_config = {
            "type": "scatter",
            "data": {
                "datasets": [
                    {
                        "label": "Quiz Scores",
                        "data": list(
                            map(
                                lambda item: {"x": item["time"], "y": item["score"]},
                                student_time_score,
                            )
                        ),
                        "borderColor": "#046A38",
                        "backgroundColor": "rgba(4, 106, 56, 0.5)",
                        "pointRadius": 6,
                    }
                ],
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "scales": {
                    "yAxes": [
                        {
                            "scaleLabel": {
                                "display": True,
                                "labelString": "Score (%)",
                            },
                            "ticks": {
                                "beginAtZero": True,
                                "max": 100,
                            },
                        }
                    ],
                    "xAxes": [
                        {
                            "scaleLabel": {
                                "display": True,
                                "labelString": "Time Taken (minutes)",
                            },
                            "ticks": {"beginAtZero": True},
                        }
                    ],
                },
            },
        }

        student_points_history_config = {
            "type": "line",
            "data": {
                "labels": student_points_history["labels"],
                "datasets": [
                    {
                        "label": f"{'Exams' if selected_quiz_mode == 'exam' else 'Practice'} Points",
                        "data": student_points_history["points"],
                        "animation": {"duration": 0},
                        "borderColor": "#046A38",
                        "backgroundColor": "rgba(4, 106, 56, 0.1)",
                        "fill": True,
                        "lineTension": 0.4,
                    }
                ],
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "scales": {
                    "yAxes": [
                        {
                            "scaleLabel": {
                                "display": True,
                                "labelString": "Points",
                            },
                        },
                    ],
                    "xAxes": [
                        {
                            "scaleLabel": {
                                "display": True,
                                "labelString": "Days",
                            },
                        },
                    ],
                },
            },
        }

        student_charts_config = {
            "type": "bar",
            "data": {
                "labels": student_charts["labels"],
                "datasets": [
                    {
                        "label": "Average Score",
                        "data": student_charts["data"],
                        "backgroundColor": [
                            "rgba(40, 167, 69, 0.7)",
                            "rgba(255, 193, 7, 0.7)",
                            "rgba(220, 53, 69, 0.7)",
                        ],
                        "borderColor": [
                            "rgb(40, 167, 69)",
                            "rgb(255, 193, 7)",
                            "rgb(220, 53, 69)",
                        ],
                        "borderWidth": 2,
                    }
                ],
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "legend": {
                        "display": False,
                    }
                },
                "legend": {
                    "display": False,
                },
                "scales": {
                    "yAxes": [
                        {
                            "scaleLabel": {
                                "display": True,
                                "labelString": "Average Score (%)",
                            },
                            "ticks": {
                                "beginAtZero": True,
                                "max": 100,
                            },
                        }
                    ]
                },
            },
        }

        student_comparision_params = {
            "chart": json.dumps(student_comparision_config),
            "width": 300,
            "height": 250,
        }

        student_points_history_params = {
            "chart": json.dumps(student_points_history_config),
            "width": 300,
            "height": 250,
        }

        student_charts_params = {
            "chart": json.dumps(student_charts_config),
            "width": 300,
            "height": 250,
        }

        student_time_score_params = {
            "chart": json.dumps(student_time_score_config),
            "width": 300,
            "height": 250,
        }
        student_quizzes["data"].sort(key=lambda x: x["date_taken"], reverse=True)

        header_mapping = {
            "take_quiz_id": "ID",
            "quiz_name": "Quiz Name",
            "quiz_mode": "Type",
            "date_taken": "Date Taken",
            "total_scored": "Score",
            "completed": "Status",
        }

        with tempfile.NamedTemporaryFile(
            delete=False, mode="w", suffix=".csv"
        ) as temp_file:
            writer = csv.writer(temp_file)

            writer.writerow(header_mapping.values())
            # Write data rows in the same column order
            for row in student_quizzes["data"]:
                writer.writerow(
                    [
                        row["take_quiz_id"],
                        row["quiz_name"],
                        row["quiz_mode"].capitalize(),
                        datetime.fromtimestamp(row["date_taken"]).strftime(
                            "%B %d, %Y %I:%M %p"
                        ),
                        (
                            f"{row['total_scored']}%" if row["total_scored"] else "NA"
                        ),  # Formatting score
                        "Completed" if row["completed"] else "Incomplete",
                    ]
                )

            temp_file_path = temp_file.name
            filename = "Quizzes taken.csv"

            if frequency == "monthly":
                filename = "Quizzes taken in the last 30 days.csv"
            elif frequency == "weekly":
                filename = "Quizzes taken in the last 7 days.csv"

        if frequency == "monthly":
            start_date = IndiaNow() - timedelta(days=30)
        elif frequency == "weekly":
            start_date = IndiaNow() - timedelta(days=7)

        end_date = IndiaNow()
        report_period = (
            f"{start_date.strftime('%b %d, %Y')} - {end_date.strftime('%b %d, %Y')}"
        )
        send_email_with_attachment(
            to=student.email,
            subject=(
                f"Monthly Activity Report"
                if frequency == "monthly"
                else "Weekly Activity Report"
            ),
            body=(
                f"This is your monthly activity report"
                if frequency == "monthly"
                else "This is your weekly activity report"
            ),
            html_body=render_template(
                "activity_report.html",
                stats=student_dashboard,
                selected_quiz_mode=selected_quiz_mode,
                student_points_history=urlencode(student_points_history_params),
                student_comparision=urlencode(student_comparision_params),
                student_charts=urlencode(student_charts_params),
                student_time_score=urlencode(student_time_score_params),
                report_period=report_period,
                frequency=frequency,
                frontend_url=os.getenv("FRONTEND_URL"),
            ),
            file_path=temp_file_path,
            filename=filename,
        )
    
    return {"message": "Activity reports sent successfully"}


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Setup periodic tasks"""
    sender.add_periodic_task(
        crontab(hour=5, minute=0),  # Every day at 5:00 AM
        send_reminder_email.s(),
        name="send_reminder_email",
    )
    sender.add_periodic_task(
        crontab(hour=5, minute=0, day_of_month=1),  # 1st of every month at 5:00 AM
        send_activity_report.s(frequency="monthly", selected_quiz_mode="exam"),
        name="send_monthly_exam_activity_report",
    )
    sender.add_periodic_task(
        crontab(hour=17, minute=0, day_of_month=1),  # 1st of every month at 5:00 PM
        send_activity_report.s(frequency="monthly", selected_quiz_mode="practice"),
        name="send_monthly_practice_activity_report",
    )
    sender.add_periodic_task(
        crontab(hour=5, minute=0, day_of_week=6),  # Sunday every week at 5:00 AM
        send_activity_report.s(frequency="weekly", selected_quiz_mode="exam"),
        name="send_weekly_exam_activity_report",
    )
    sender.add_periodic_task(
        crontab(hour=17, minute=0, day_of_week=6),  # Sunday every week at 5:00 PM
        send_activity_report.s(frequency="weekly", selected_quiz_mode="practice"),
        name="send_weekly_practice_activity_report",
    )
