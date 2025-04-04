from flask_restx import Namespace, fields

contact_ns = Namespace('contact', description="Contact API")

create_contact_model = contact_ns.model('CreateContact', {
    'name': fields.String(required=True),
    'email': fields.String(required=True),
    'message': fields.String(required=True)
})