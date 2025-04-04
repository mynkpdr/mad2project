from flask import request
from app.api.api_models.question import question_ns, create_question_model, get_questions_model, get_question_model
from flask_restx import Resource
from app.extensions import db
from werkzeug.exceptions import NotFound
from app.utils.custom import validate_fields
from app.models import CorrectAnswer, Option, Question, Chapter
from app.decorators import admin_required


# User API Resource
@question_ns.route("")
class QuestionResource(Resource):
    @question_ns.expect(create_question_model)
    @admin_required
    def post(self):
        """Create a question"""
        # Extract payload
        payload = question_ns.payload
        chapter_id = payload.get("chapter_id")
        question_type = payload.get(
            "question_type"
        )
        question_statement = payload.get("question_statement")
        options = payload.get("options")
        question_image = payload.get("question_image")
        answer_explanation = payload.get("answer_explanation")
        correct_answer = payload.get("correct_answer")
        correct_answers = payload.get("correct_answers")
        numerical_answer = payload.get("numerical_answer")
        marks = payload.get("marks", 1)
        validate_fields(
            [
                ("marks", marks, True),
                ("chapter_id", chapter_id, True),
                ("question_type", question_type, True),
                ("question_statement", question_statement, True),
                ("answer_explanation", answer_explanation, False),
            ]
        )

        chapter_data = Chapter.query.get(chapter_id)
        if not chapter_data:
            raise NotFound(f"Chapter with ID {chapter_id} not found.")
        if question_type.upper() in ["MCQ", "MSQ", "NUMERICAL"]:
            new_question = Question(
                question_statement=question_statement,
                answer_explanation=answer_explanation,
                question_type=question_type.upper(),
                chapter_id=chapter_data.id,
                question_image=question_image,
                marks=marks,
            )
            db.session.add(new_question)

        if question_type.upper() == "MCQ":
            for index, option in enumerate(options):
                new_option = Option(
                    question=new_question,
                    option_text=option,
                    is_correct=True if index == correct_answer else False,
                )
                if index == correct_answer:
                    new_correct_answer = CorrectAnswer(
                        question=new_question,
                        answer_text=options[correct_answer],
                        option=new_option,
                    )
                    db.session.add(new_correct_answer)
                db.session.add(new_option)

        elif question_type.upper() == "MSQ":
            for index, option in enumerate(options):
                new_option = Option(
                    question=new_question,
                    option_text=option,
                    is_correct=True if index in correct_answers else False,
                )
                if index in correct_answers:
                    new_correct_answer = CorrectAnswer(
                        question=new_question,
                        answer_text=options[index],
                        option=new_option,
                    )
                    db.session.add(new_correct_answer)
                db.session.add(new_option)
        else:
            new_correct_answer = CorrectAnswer(
                answer_text=numerical_answer, question=new_question
            )
            db.session.add(new_correct_answer)
        db.session.commit()
        return {"success": True}, 201

    @question_ns.marshal_with(get_questions_model)
    @admin_required
    def get(self):
        """Get all questions"""
        questions = Question.query.all()
        response = []

        for index, question in enumerate(questions):
            response.append(
                {
                    "id": question.id,
                    "display_id": index + 1,
                    "question_image": question.question_image,
                    "answer_explanation": question.answer_explanation,
                    "statement": question.question_statement,
                    "type": question.question_type.value,
                    "marks": question.marks,
                    "date_created": question.date_created,
                    "options": [
                        {
                            "id": option.id,
                            "text": option.option_text,
                            "is_correct": option.is_correct,
                        }
                        for option in question.options
                    ],
                    "correct_answers": [
                        ca.answer_text for ca in question.correct_answers
                    ],
                }
            )
        return {"data": response}, 200


@question_ns.route("/<int:id>")
class SingleQuestionResource(Resource):
    @question_ns.marshal_with(get_question_model)
    @admin_required
    def get(self, id):
        """Get a question"""
        question = Question.query.get(id)
        if not question:
            raise NotFound(f"Question with id {id} not found")
        subject_id = Chapter.query.get(question.chapter_id).subject_id
        if not subject_id:
            raise NotFound(f"Subject with ID {subject_id} not found")

        option_map = {option.id: option.option_text for option in question.options}
        response = {
            "id": question.id,
            "chapter_id": question.chapter_id,
            "subject_id": subject_id,
            "statement": question.question_statement,
            "answer_explanation": question.answer_explanation,
            "question_image": question.question_image,
            "type": question.question_type.value,
            "marks": question.marks,
            "date_created": question.date_created,
            "options": [
                {
                    "id": option.id,
                    "text": option.option_text,
                    "is_correct": any(
                        ca.option_id == option.id for ca in question.correct_answers
                    ),
                }
                for option in question.options
            ],
            "correct_answers": [
                option_map[ca.option_id] if ca.option_id else ca.answer_text
                for ca in question.correct_answers
            ],
        }
        return {"data": response}, 200

    @question_ns.expect(create_question_model)
    @admin_required
    def put(self, id):
        """Update a question"""
        # Extract payload
        question = Question.query.get(id)
        if not question:
            raise NotFound(f"Question with id {id} not found")
        payload = question_ns.payload
        chapter_id = payload.get("chapter_id", question.chapter_id)
        question_type = payload.get(
            "question_type", question.question_type.value
        )
        question_statement = payload.get("question_statement", question.question_statement)
        answer_explanation = payload.get("answer_explanation", question.answer_explanation)
        options = payload.get("options", [option.option_text for option in question.options])
        question_image = payload.get("question_image", question.question_image)
        correct_answer = payload.get("correct_answer")
        correct_answers = payload.get("correct_answers")
        numerical_answer = payload.get("numerical_answer")
        marks = payload.get("marks", question.marks)
        validate_fields(
            [
                ("chapter_id", chapter_id, True),
                ("question_type", question_type, True),
                ("question_statement", question_statement, True),
                ("marks", marks, True),
                ("answer_explanation", answer_explanation, False),
            ]
        )

        chapter_data = Chapter.query.get(chapter_id)
        if not chapter_data:
            raise NotFound(f"Chapter with ID {chapter_id} not found.")
        if question_type.upper() in ["MCQ", "MSQ", "NUMERICAL"]:
            question.chapter_id = chapter_id
            question.question_type = question_type.upper()
            question.question_statement = question_statement
            question.answer_explanation = answer_explanation
            question.question_image = question_image
            question.marks = marks
            for option in question.options:
                db.session.delete(option)
            for ca in question.correct_answers:
                db.session.delete(ca)
            db.session.commit()

        if question_type.upper() == "MCQ":
            for index, option in enumerate(options):
                new_option = Option(
                    question=question,
                    option_text=option,
                    is_correct=True if index == correct_answer else False,
                )
                if index == correct_answer:
                    new_correct_answer = CorrectAnswer(
                        question=question,
                        answer_text=options[correct_answer],
                        option=new_option,
                    )
                    db.session.add(new_correct_answer)
                db.session.add(new_option)

        elif question_type.upper() == "MSQ":
            for index, option in enumerate(options):
                new_option = Option(
                    question=question,
                    option_text=option,
                    is_correct=True if index in correct_answers else False,
                )
                if index in correct_answers:
                    new_correct_answer = CorrectAnswer(
                        question=question,
                        answer_text=options[index],
                        option=new_option,
                    )
                    db.session.add(new_correct_answer)
                db.session.add(new_option)
        else:
            new_correct_answer = CorrectAnswer(
                answer_text=numerical_answer, question=question
            )
            db.session.add(new_correct_answer)
        db.session.commit()

        return {"success": True}, 201

    @admin_required
    def delete(self, id):
        """Delete a question"""
        question = Question.query.get(id)
        if not question:
            raise NotFound(f"Question with id {id} not found")

        db.session.delete(question)
        db.session.commit()
        return {"success": True}, 200
