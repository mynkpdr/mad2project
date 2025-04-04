from app.api.api_models.contact import contact_ns, create_contact_model
from flask_restx import Resource
from app.extensions import db
from werkzeug.exceptions import NotFound
from app.utils.custom import validate_fields
from app.models.contact import Contact
from app.tasks import send_email_async
from app.decorators import admin_required

@contact_ns.route("")
class ContactResource(Resource):
    @contact_ns.expect(create_contact_model)
    def post(self):
        """Create a contact message"""
        payload = contact_ns.payload
        name = payload.get('name')
        email = payload.get('email')
        message = payload.get('message')
        validate_fields([
            ("name", name, True),
            ("email", email, True),
            ("message", message, True)
            ])
        contact = Contact(name=name, email=email, message=message)
        db.session.add(contact)
        db.session.commit()
        task = send_email_async.delay(
            to="email_address of the admin",
            subject="New message from ExamBhai",
            body=f"Name: {name}\nEmail: {email}\nMessage: {message}",
            html_body=f"<p>Name: {name}</p><p>Email: {email}</p><p>Message: {message}</p>",
        )
        return {"message": "Message sent successfully", "task_id": task.id}, 201
    
    @admin_required
    def get(self):
        """Get all contact messages"""
        contacts = Contact.query.all()
        response = []
        for contact in contacts:
            response.append({
                "id": contact.id,
                "name": contact.name,
                "email": contact.email,
                "message": contact.message,
                "date_created": contact.date_created
            })
        return {"data": response}, 200

@contact_ns.route("/<int:id>")
class SingleContactResource(Resource):
    @admin_required
    def get(self, id):
        """Get a contact message"""
        contact = Contact.query.get(id)
        if not contact:
            raise NotFound(f"Contact with id {id} not found")
        response = {
            "id": contact.id,
            "name": contact.name,
            "email": contact.email,
            "message": contact.message,
            "date_created": contact.date_created
        }
        return {"data": response}, 200
    
    @admin_required
    def delete(self, id):
        """Delete a contact message"""
        contact = Contact.query.get(id)
        if not contact:
            raise NotFound(f"Contact with id {id} not found")
        db.session.delete(contact)
        db.session.commit()
        return{"Success": True}, 200
    