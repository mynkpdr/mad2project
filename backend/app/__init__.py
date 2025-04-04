from flask import Flask
from app.config import config_options
from app.extensions import db, cors, migrate, mail, jwt, bcrypt, cache
from app.api import api
import os
from app.models import db, Student, User, Subject, Chapter, Quiz, Question, Option, CorrectAnswer, Admin, QuestionType, Student, DifficultyLevel, QuizMode
from werkzeug.exceptions import Unauthorized
from app.utils.timezone import IndiaTimeStampNow
def create_app():
    app = Flask(__name__)
    app.config.from_object(config_options[os.getenv("FLASK_CONFIG", "default")])
    register_extensions(app)
    def unauthorized_callback(callback):
        raise Unauthorized("Missing Authorization Header")
    jwt.unauthorized_loader(unauthorized_callback)
    app.errorhandler(Exception)(lambda e: ({"message": str(e) if e else "An Error Occured"}, getattr(e, "code", 500)))
    question_image_folder = os.getenv("QUESTION_IMAGE_UPLOAD_FOLDER")
    profile_picture_folder = os.getenv("PROFILE_PICTURE_UPLOAD_FOLDER")

    # Ensure the directory exists
    if not os.path.exists(profile_picture_folder):
        os.makedirs(profile_picture_folder, exist_ok=True)
    if not os.path.exists(question_image_folder):
        os.makedirs(question_image_folder, exist_ok=True)

    with app.app_context():
        db.drop_all()
        db.create_all()
        # Create Admin Users
        admin1 = User(
            username="admin1",
            password="12345678",
            gender="Male",
            name="Admin One",
            email="admin@email.com",
            role="ADMIN",
            email_verified=True
        )
        admin2 = User(
            username="admin2",
            password="admin123!",
            gender="Female",
            name="Admin Two",
            email="admin2@email.com",
            role="ADMIN",
            email_verified=True
        )
        db.session.add_all([admin1, admin2])
        db.session.commit()
        admin_admin1 = Admin(user_id=admin1.id)
        admin_admin2 = Admin(user_id=admin2.id)
        db.session.add_all([admin_admin1, admin_admin2])
        # Create Regular Users
        student_names = [
            ("John", "Doe"), ("Emma", "Wilson"), ("Alex", "Smith"), ("Sarah", "Parker"),
            ("Mike", "Brown"), ("Lisa", "Jones"), ("David", "Miller"), ("Anna", "White"),
            ("James", "Taylor"), ("Emily", "Davis"), ("Robert", "Martin"), ("Laura", "Anderson"),
            ("Thomas", "Moore"), ("Jessica", "Clark"), ("Daniel", "Lee"), ("Rachel", "Walker"),
            ("Kevin", "Hall"), ("Sophie", "Wright"), ("Peter", "Scott"), ("Maria", "Green")
        ]
        
        users = []
        for i, (first, last) in enumerate(student_names):
            username = f"{first.lower()}_{last.lower()}"
            users.append(User(
                username=username,
                email_verified=True,
                password="12345678",
                name=f"{first} {last}",
                gender="Male" if i % 2 == 0 else "Female",
                role="STUDENT",
                email=f"{username}@email.com" if i != 0 else "user@email.com"
            ))
        db.session.add_all(users)
        db.session.commit()
    
        # Create Student profiles
        qualifications = ["B.Tech", "M.Sc", "B.Sc", "M.Tech", "B.E"]
        branches = ["Computer Science", "Physics", "Mathematics", "Electronics", "Mechanical", 
                   "Chemistry", "Biology", "IT", "Civil", "Electrical"]
        
        students = []
        for i, user in enumerate(users):
            qual = qualifications[i % len(qualifications)]
            branch = branches[i % len(branches)]
            student = Student(user_id=user.id, qualification=f"{qual} {branch}")
            students.append(student)
        db.session.add_all(students)
        db.session.commit()  # Commit to ensure students have IDs
        print("Admin and Student users created!")
    
        # Create Subjects (15)
        subject_data = [
            "Mathematics", "Physics", "Chemistry", "Biology", "Computer Science",
            "Electronics", "Mechanical Engineering", "Civil Engineering", "Economics",
            "Statistics", "Psychology", "Environmental Science", "Geology", 
            "Astronomy", "Information Technology"
        ]
        
        subjects = [Subject(name=name, description=f"Study of {name}") for name in subject_data]
        db.session.add_all(subjects)
    
        # Create Chapters (30)
        chapter_data = []
        for subject in subjects:
            chapter_data.extend([
                (f"{subject.name} - Chapter {i+1}", f"Description for {subject.name} Chapter {i+1}", subject)
                for i in range(2)  # 2 chapters per subject = 30 total
            ])
        
        chapters = [Chapter(name=name, description=desc, subject=subj) 
                    for name, desc, subj in chapter_data]
        db.session.add_all(chapters)
        print("Subjects and Chapters created!")
    
        # Create Quizzes (10)
        quizzes = []
        for i in range(10):
            chapter = chapters[i % len(chapters)]
            mode = QuizMode.EXAM if i % 2 == 0 else QuizMode.PRACTICE
            if i % 4 == 0:
                difficulty_level = DifficultyLevel.EASY 
            elif i % 4 == 1:
                difficulty_level = DifficultyLevel.MEDIUM
            elif i % 4 == 2:
                difficulty_level = DifficultyLevel.HARD
            else:
                difficulty_level = DifficultyLevel.UNSET
    
            quizzes.append(Quiz(
                name=f"{chapter.name} Quiz",
                chapter=chapter,
                time_duration=(30 + i * 10) * 60 if i > 3 else 60 + i * 60,
                description=f"Quiz for {chapter.name}",
                difficulty_level=difficulty_level,
                date_of_quiz=IndiaTimeStampNow() if i < 5 else IndiaTimeStampNow() + (i * 10 if i > 3 else i * 20 * 60),
                quiz_mode=mode
            ))
        db.session.add_all(quizzes)
        print("Quizzes created!")
    
        # Create Questions (50)
        questions = []
        options = []
        correct_answers = []
    
        # 30 MCQ Questions
        for i in range(30):
            chapter = chapters[i % len(chapters)]
            q = Question(
                chapter=chapter,
                question_statement=f"MCQ Question {i+1} for {chapter.name}",
                question_type=QuestionType.MCQ,
                answer_explanation=f"Explanation for MCQ Question {i+1}" if i % 2 == 0 else None
            )
            questions.append(q)
            
            opts = [
                Option(question=q, option_text=f"Option {j+1}", is_correct=(j==0))
                for j in range(4)
            ]
            options.extend(opts)
            correct_answers.append(CorrectAnswer(question=q, answer_text=opts[0].option_text, option=opts[0]))
    
        # 10 MSQ Questions
        for i in range(10):
            chapter = chapters[i % len(chapters)]
            q = Question(
                chapter=chapter,
                question_statement=f"MSQ Question {i+1} for {chapter.name}",
                question_type=QuestionType.MSQ,
                answer_explanation=f"Explanation for MSQ Question {i+1}" if i % 2 == 0 else None
            )
            questions.append(q)
            
            opts = [
                Option(question=q, option_text=f"Option {j+1}", is_correct=(j<2))
                for j in range(4)
            ]
            options.extend(opts)
            for opt in opts[:2]:  # First two options are correct
                correct_answers.append(CorrectAnswer(question=q, answer_text=opt.option_text, option=opt))
    
        # 10 Numerical Questions
        for i in range(10):
            chapter = chapters[i % len(chapters)]
            q = Question(
                chapter=chapter,
                question_statement=f"Numerical Question {i+1} for {chapter.name}",
                question_type=QuestionType.NUMERICAL,
                answer_explanation=f"Explanation for Numerical Question {i+1}" if i % 2 == 0 else None
            )
            questions.append(q)
            correct_answers.append(CorrectAnswer(question=q, answer_text=str(i*10)))
    
        db.session.add_all(questions)
        db.session.add_all(options)
        db.session.add_all(correct_answers)
        db.session.commit()
        print("Questions created!")
    return app


def register_extensions(app):
    """Registers flask extensions"""
    db.init_app(app)
    api.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
