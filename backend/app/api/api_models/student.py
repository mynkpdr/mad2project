from flask_restx import Namespace, fields

student_ns = Namespace("students", description="Student related operations")

StudentModel = student_ns.model(
    "StudentModel",
    {
        "id": fields.Integer(description="Student's ID"),
        "username": fields.String(description="Username of the student"),
        "name": fields.String(description="Full name of the student"),
        "email": fields.String(description="Email address of the student"),
        "phone_number": fields.String(description="Phone number of the student"),
        "address": fields.String(description="Address of the student"),
        "gender": fields.String(description="Gender of the student"),
        "dob": fields.Integer(description="Date of birth (UNIX timestamp)"),
        "profile_picture": fields.String(description="Profile picture URL"),
        "date_created": fields.Integer(description="Account creation timestamp"),
        "last_login": fields.Integer(description="Last login timestamp"),
        "role": fields.String(description="Role of the student"),
        "status": fields.String(description="Status of the student"),
        "bio": fields.String(description="Short biography of the student"),
        "email_verified": fields.Boolean(
            description="Is the student's email verified?"
        ),
        "qualification": fields.String(
            description="Highest qualification of the student"
        ),
    },
)

get_students_model = student_ns.model(
    "GetStudent", {"data": fields.List(fields.Nested(StudentModel))}
)

get_student_model = student_ns.model(
    "GetStudents", {"data": fields.Nested(StudentModel)}
)

create_student_model = student_ns.model(
    "CreateStudent",
    {
        "username": fields.String(required=True),
        "name": fields.String(required=True),
        "email": fields.String(required=True),
        "phone_number": fields.String,
        "address": fields.String,
        "gender": fields.String,
        "dob": fields.DateTime,
        "profile_picture": fields.String,
        "password": fields.String(required=True),
        "bio": fields.String,
        "qualification": fields.String,
    },
)
