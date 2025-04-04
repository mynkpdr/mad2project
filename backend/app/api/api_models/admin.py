from flask_restx import Namespace, fields

admin_ns = Namespace('admins', description='Admin related operations')

adminModel = admin_ns.model(
    'AdminModel',
    {
        'id': fields.Integer(description='Admin ID'),
        'username': fields.String(description='Username of the admin'),
        'name': fields.String(description='Full name of the admin'),
        'email': fields.String(description='Email address of the admin'),
        'status': fields.String(description='Status of the admin'),
        'email verified': fields.String(description="Is the admin's email verified?"),
        'date_created': fields.Integer(description='Account creation timestamp'),
    }
)

adminDashboardModel = admin_ns.model(
    'AdminDashboardModel',
    {
        'total_students': fields.Integer(description='Total number of students'),
        'total_quizzes': fields.Integer(description='Total number of quizzes'),
        'active_students': fields.Integer(description='Number of active students'),
        'quizzes_completed': fields.Integer(description='Number of quizzes completed'),
        'difficulty_level_distribution': fields.Raw(description='Distribution of difficulty levels'),
    }
)

get_admins_model = admin_ns.model(
    'GetAdmins',
    {'data': fields.List(fields.Nested(adminModel))}
)

# get_admin_model = admin_ns.model(
#     'GetAdmin',
#     fields.Nested(adminModel)
# )