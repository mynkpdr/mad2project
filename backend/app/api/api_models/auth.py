from flask_restx import fields, Namespace

auth_ns = Namespace("auth", description="Authentication APIs")

login_model = auth_ns.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
})

signup_model = auth_ns.model('Signup', {
    'username': fields.String(required=False),
    'name': fields.String(required=True),
    'email': fields.String(required=True),
    'phone_number': fields.String,
    'address': fields.String,
    'gender': fields.String,
    'dob': fields.DateTime,
    'profile_picture': fields.String,
    'password': fields.String(required=True),
    'bio': fields.String,
    'qualification': fields.String,
})

forgot_password_model = auth_ns.model('ForgotPassword', {
    'email':fields.String(required=True)
})