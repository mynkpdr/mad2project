from flask_restx import Namespace, fields

question_ns = Namespace('questions', description='Question related operations')

create_question_model = question_ns.model('CreateQuestion', {
    'chapter_id': fields.Integer(required=True, description="ID of the chapter"),
    'question_type': fields.String(required=True, description="Type of question (MCQ, MSQ, NUMERICAL)"),
    'question_statement': fields.String(required=True, description="The question text"),
    'options': fields.List(fields.String, required=False, description="List of options for MCQ/MSQ"),
    'question_image': fields.String(required=False, description="URL of the question image"),
    'answer_explanation': fields.String(required=False, description="Explanation for the answer"),
    'correct_answer': fields.Integer(required=False, description="Index of the correct answer for MCQ"),
    'correct_answers': fields.List(fields.Integer, required=False, description="Indices of correct answers for MSQ"),
    'numerical_answer': fields.Float(required=False, description="Numerical answer for NUMERICAL questions"),
    'marks': fields.Integer(required=False, description="Marks for the question")
})


question_model = question_ns.model('QuestionModel', {
    'id': fields.Integer(description="ID of the question"),
    'chapter_id': fields.Integer(description="ID of the chapter"),
    'subject_id': fields.Integer(description="ID of the subject"),
    'display_id': fields.Integer(description="Display ID of the question"),
    'question_image': fields.String(description="URL of the question image"),
    'answer_explanation': fields.String(description="Explanation for the answer"),
    'statement': fields.String(description="The question text"),
    'type': fields.String(description="Type of question (MCQ, MSQ, NUMERICAL)"),
    'marks': fields.Integer(description="Marks for the question"),
    'date_created': fields.Integer(description="Date when the question was created"),
    'options': fields.List(fields.Nested(question_ns.model('Option', {
        'id': fields.Integer(description="ID of the option"),
        'text': fields.String(description="Text of the option"),
        'is_correct': fields.Boolean(description="Whether the option is correct")
    })), description="List of options for the question"),
    'correct_answers': fields.List(fields.String, description="List of correct answers")
})

get_questions_model = question_ns.model('GetQuestions', {
    'data': fields.List(fields.Nested(question_model))
})

get_question_model = question_ns.model('GetQuestion', {
    'data': fields.Nested(question_model)
})