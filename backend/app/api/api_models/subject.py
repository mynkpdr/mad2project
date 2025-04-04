from flask_restx import Namespace, fields

subject_ns = Namespace('subjects', description='Subject related operations')

create_subject_model = subject_ns.model('CreateSubject', {
    'name': fields.String(required=True),
    'description': fields.String(required=True)
})