from flask_mail import Message
from app.extensions import mail

def send_email(to, subject, body, html_body):
    """
    Utility function to send emails.
    """
    msg = Message(subject, recipients=[to], body=body, html=html_body)
    mail.send(msg)
