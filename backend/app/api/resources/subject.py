from flask import request
from flask_jwt_extended import jwt_required
from app.api.api_models.subject import subject_ns
from flask_restx import Resource
from app.extensions import db
from app.utils.custom import validate_fields
from app.models.subject import Subject
from werkzeug.exceptions import NotFound

from app.decorators import admin_required


# User API Resource
@subject_ns.route("")
class SubjectResource(Resource):
    @admin_required
    def post(self):
        """Create a subject"""
        payload = subject_ns.payload
        name = payload.get("name")
        description = payload.get("description")

        validate_fields([("name", name, True), ("description", description, True)])
        new_subject = Subject(name=name, description=description)
        db.session.add(new_subject)
        db.session.commit()
        return {"message": "Successfully created a new subject"}, 201

    @jwt_required()
    def get(self):
        subjects = Subject.query.all()
        response = [
            {
                "id": subject.id,
                "name": subject.name,
                "description": subject.description,
                "date_created": subject.date_created,
                "chapters": [
                    {"id": chapter.id, "name": chapter.name}
                    for chapter in subject.chapters
                ],
            }
            for subject in subjects
        ]

        return {"data": response}, 200


@subject_ns.route("/<int:id>")
class SingleSubjectResource(Resource):
    @jwt_required()
    def get(self, id):
        """Get a subject"""
        subject = Subject.query.get(id)
        if not subject:
            raise NotFound(f"Subject with id {id} not found")
        response = {
            "id": subject.id,
            "name": subject.name,
            "description": subject.description,
            "date_created": subject.date_created,
            "chapters": [
                {
                    "id": chapter.id,
                    "name": chapter.name,
                    "date_created": chapter.date_created,
                    "questions_count": len(chapter.questions),
                }
                for chapter in subject.chapters
            ],
        }
        return {"data": response}, 200

    @admin_required
    def put(self, id):
        """Edit a subject"""
        subject = Subject.query.get(id)
        if not subject:
            raise NotFound(f"Subject with id {id} not found")
        payload = subject_ns.payload
        name = payload.get("name", subject.name)
        description = payload.get("description", subject.description)

        validate_fields([("name", name, True), ("description", description, True)])

        subject.description = description
        subject.name = name
        db.session.commit()
        return {"success": True}, 200

    @admin_required
    def delete(self, id):
        """Delete a subject"""
        subject = Subject.query.get(id)
        if not Subject:
            raise NotFound(f"Subject with id {id} not found")

        db.session.delete(subject)
        db.session.commit()
        return {"success": True}, 200
