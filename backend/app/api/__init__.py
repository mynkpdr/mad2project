import os
from flask_restx import Api
from flask import Blueprint
from app.api.resources.quiz import quiz_ns
from app.api.resources.student import student_ns
from app.api.resources.admin import admin_ns
from app.api.resources.user import user_ns
from app.api.resources.auth import auth_ns
from app.api.resources.question import question_ns
from app.api.resources.subject import subject_ns
from app.api.resources.chapter import chapter_ns
from app.api.resources.contact import contact_ns
from app.api.resources.take_quiz import take_quiz_ns
from app.api.resources.main import main_ns
from app.api.resources.export import export_ns
from app.api.resources.task import task_ns

api_bp = Blueprint("api", __name__)

api = Api(
    version="1.0",
    title="ExamBhai Swagger API",
    doc="/swagger",
    description="ExamBhai Swagger API for managing students and quizzes",
    contact="Mayank Kumar Poddar",
    terms_url=f'{os.getenv("FRONTEND_URL")}/terms',
    contact_url="https://mynkpdr.github.io",
    contact_email="23f3004197@ds.study.iitm.ac.in",
    authorizations={
        "api_key": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "JWT Authorization header using the Bearer scheme. Example usage: 'Bearer [JWT]'",
        },
    },
    security="api_key",
)
api.add_namespace(task_ns, path="/api/task")
api.add_namespace(export_ns, path="/api/export")
api.add_namespace(take_quiz_ns, path="/api/take_quiz")
api.add_namespace(contact_ns, path="/api/contacts")
api.add_namespace(chapter_ns, path="/api/chapters")
api.add_namespace(subject_ns, path="/api/subjects")
api.add_namespace(question_ns, path="/api/questions")
api.add_namespace(quiz_ns, path="/api/quizzes")
api.add_namespace(user_ns, path="/api/users")
api.add_namespace(student_ns, path="/api/students")
api.add_namespace(admin_ns, path="/api/admins")
api.add_namespace(auth_ns, path="/api/auth")
api.add_namespace(main_ns, path="/api")
