from flask_restx import Namespace, fields

chapter_ns = Namespace('chapters', description='Chapter related operations')

create_chapter_model = chapter_ns.model('CreateChapter', {
    'name': fields.String(required=True),
    'description': fields.String(required=True),
    'subject_id': fields.Integer(required=True),
})