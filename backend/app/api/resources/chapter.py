from app.api.api_models.chapter import chapter_ns, create_chapter_model
from flask_restx import Resource
from app.extensions import db
from werkzeug.exceptions import NotFound
from app.utils.custom import validate_fields
from app.models import Chapter, Subject
from app.decorators import admin_required


# User API Resource
@chapter_ns.route("")
class ChapterResource(Resource):
    @chapter_ns.expect(create_chapter_model)
    @admin_required
    def post(self):
        """Create a chapter"""
        # Extract payload
        payload = chapter_ns.payload
        name = payload.get("name")
        description = payload.get("description")
        subject_id = payload.get("subject_id")
        validate_fields(
            [
                ("name", name, True),
                ("description", description, True),
                ("subject_id", subject_id, True),
            ]
        )
        subject = Subject.query.get(subject_id)
        if not subject:
            raise NotFound(f"Subject with ID {subject_id} not found")
        new_chapter = Chapter(
            name=name, description=description, subject_id=subject.id
        )
        db.session.add(new_chapter)
        db.session.commit()

        return {"success": True}, 201

    def get(self):
        chapters = Chapter.query.all()
        response = []
        for chapter in chapters:
            response.append(
                {
                    "id": chapter.id,
                    "name": chapter.name,
                    "description": chapter.description,
                    "questions_count": len(chapter.questions),
                    "date_created": chapter.date_created,
                }
            )
        return {"data": response}, 200


@chapter_ns.route("/<int:id>")
class SingleChapterResource(Resource):
    @admin_required
    def get(self, id):
        """Get a chapter"""
        chapter = Chapter.query.get(id)
        if not chapter:
            raise NotFound(f"Chapter with id {id} not found")
        response = {
            "id": chapter.id,
            "name": chapter.name,
            "subject_id": chapter.subject.id,
            "subject_name": chapter.subject.name,
            "description": chapter.description,
            "date_created": chapter.date_created,
            "questions": [
                {
                    "id": question.id,
                    "marks": question.marks,
                    "question_statement": question.question_statement,
                    "question_image": question.question_image,
                    "date_created": question.date_created,
                    "question_type": question.question_type.value,
                }
                for question in chapter.questions
            ],
        }
        return {"data": response}, 200

    @admin_required
    def put(self, id):
        """Edit a chapter"""
        payload = chapter_ns.payload
        name = payload.get("name")
        description = payload.get("description")

        validate_fields([("name", name, True), ("description", description, True)])
        chapter = Chapter.query.get(id)
        if not chapter:
            raise NotFound(f"Chapter with id {id} not found")
        chapter.description = description
        chapter.name = name
        db.session.commit()
        return {"success": True}, 200

    @admin_required
    def delete(self, id):
        """Delete a chapter"""
        chapter = Chapter.query.get(id)
        if not chapter:
            raise NotFound(f"Chapter with id {id} not found")

        db.session.delete(chapter)
        db.session.commit()
        return {"success": True}, 200
