import tempfile
import os
from datetime import datetime
from flask_mail import Message
from app.extensions import mail
from werkzeug.exceptions import InternalServerError
def send_email_with_attachment(to, subject, body, html_body, file_path, filename):
    """Send an email with an attachment"""
    msg = Message(subject, recipients=[to], body=body, html=html_body)

    with open(file_path, 'r') as f:
        msg.attach(filename, 'text/html', f.read())
        
    mail.send(msg)
    # Cleanup temporary file
    cleanup_export_file(file_path)

def export_to_file(data, export_type):
    """Create a temporary file and write the export data to it"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=f'.{export_type}') as temp_file:
        temp_file.write(data)
        temp_file_path = temp_file.name
    
    return {
        'file_path': temp_file_path,
        'filename': f'export_{timestamp}.{export_type}'
    }

def cleanup_export_file(file_path):
    """Clean up the temporary export file"""
    try:
        os.remove(file_path)
    except OSError as e:
        raise InternalServerError("Error cleaning up export file")
