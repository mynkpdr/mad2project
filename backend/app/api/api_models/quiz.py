from flask_restx import Namespace, fields

quiz_ns = Namespace('quizzes', description='Quiz related operations')

quiz_model = quiz_ns.model('Quiz', {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'chapter_id': fields.Integer,
    'difficulty_level': fields.String,
    'date_of_quiz': fields.DateTime,
    'time_duration': fields.String
})


create_quiz_model = quiz_ns.model('CreateQuiz', {
    'name': fields.Integer(required=True),
    'description': fields.String,
    'chapter_id': fields.Integer(required=True),
    'date_of_quiz': fields.DateTime,
    'difficulty_level': fields.String,
    'time_duration': fields.Integer(required=True),
    'description': fields.String
})