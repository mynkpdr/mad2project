from flask import render_template
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from app.utils.export import export_to_file
from werkzeug.exceptions import BadRequest
from app.tasks import send_email_with_attachment_async
export_ns = Namespace('export', description='Export operations')

@export_ns.route('/email')
class ExportEmailResource(Resource):
    @jwt_required()
    def post(self):
        """Send export data via email asynchronously"""
        try:
            user = User.query.get(get_jwt_identity())
            data = export_ns.payload
            
            export_data = data.get('data')
            export_type = data.get('type')
            if not export_data or not export_type:
                raise BadRequest('Missing required data')
            
            # Create temporary file
            export_file = export_to_file(export_data, export_type)
            
            # Send email with attachment asynchronously
            subject = f'Your {export_type.upper()} Export from Exambhai'
            task = send_email_with_attachment_async.delay(
                to=user.email,
                subject=subject,
                body="Please find your requested export file attached.",
                file_path=export_file['file_path'],
                filename=export_file['filename'],
                html_body=render_template('export.html')
            )
            return {'message': f'Export data will be sent to {user.email}', 'task_id': task.id}, 200
                
        except Exception as e:
            raise Exception('Failed to process export request' + str(e))
