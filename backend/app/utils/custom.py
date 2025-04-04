from datetime import datetime
import math
import random
from app.models import User
import re

prefix_usernames = [
    "PadhakuShikari",
    "GyaanKaJadoo",
    "ToppersMunda",
    "StudyMaharaja",
    "PadhaiPanda",
    "GyaanWala",
    "ExamMasterji",
    "ShabashBabu",
    "PadhakuJatt",
    "GyaanSeekerJi",
    "KitabiSher",
    "PadhaiWalaRaja",
    "ExamKingji",
    "ToppersBabu",
    "GyaanMaharaja",
    "KitabiChampion",
    "BrainyMunde",
    "ExamKaBaap",
    "StudyJugaad",
    "GyaanKundli"
]

def generate_unique_username():
    """Generate a unique username"""
    prefix_username = random.choice(prefix_usernames)
    while True:
        suffix_number = random.randint(00000, 99999) # The website can have 2000000 users with such username
        username = f"{prefix_username}_{suffix_number}"
        if not User.query.filter_by(username=username).first():
            break
    return username

def calculate_points(avg_score, avg_time, total_quizzes):
    """Calculate points based on the average score, average time, and total quizzes"""
    # Calculate weighted points
    W1, W2, W3 = 0.5, 0.3, 0.2  # Weights for score, time, and volume
    # points_earned = (avg_score * 0.5) + (1 / (avg_time + 1) * 100 * 0.3) + (math.log(total_quizzes + 1) * 10 * 0.2)
    score_component = avg_score * W1
    time_efficiency = (
        (1 / (avg_time + 1)) * 100 * W2 if avg_time else 0
    )  # Add 1 to avoid division by zero
    volume_component = (
        math.log(total_quizzes + 1) * 10
    ) * W3  # Add 1 to avoid log(0) :()
    return int(score_component + time_efficiency + volume_component)

def validate_fields(fields):
    """Validate the fields based on the rules provided"""
    for field, value, required in fields:
        if required and not value:
            raise ValueError(f"{field} is required")
        if value:
            if field == "email":
                if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                    raise ValueError("Invalid email format")
            elif field == "username":
                if not len(str(value)) >= 3:
                    raise ValueError(f"{field} should be greater than or equal to 3 letters.")
            elif field == "password" or field == "new_password" or field == "current_password":
                if not len(str(value)) >= 8:
                    raise ValueError(f"{field} should be at least 8 characters long.")
            elif field == "phone_number":
                if not len(str(value)) >=10:
                    raise ValueError(f"{field} should be at least 10 numbers long.")
            elif field == "gender":
                if value.upper() not in ["MALE", "FEMALE"]:
                    raise ValueError(f"{field} should be one of ['MALE', 'FEMALE'].")
            elif field == "question_type":
                if value.upper() not in ["MCQ", "MSQ", "NUMERICAL"]:
                    raise ValueError(f"{field} should be one of ['MCQ', 'MSQ', 'NUMERICAL'].")
            elif field == "difficulty_level":
                if value.upper() not in ["EASY", "MEDIUM", "HARD", "UNSET"]:
                    raise ValueError(f"{field} should be one of ['EASY', 'MEDIUM', 'HARD', 'UNSET'].")
            elif field == "status":
                if value.upper() not in ["ACTIVE", "SUSPENDED"]:
                    raise ValueError(f"{field} should be one of ['ACTIVE', 'SUSPENDED'].")
            elif field == "date_of_quiz":
                try:
                    doq = datetime.strptime(value, "%Y-%m-%dT%H:%M")  # Expecting the format 'YYYY-MM-DD-HH-MM'
                    date_of_quiz = int(doq.timestamp())
                except ValueError:
                    raise ValueError(f"Invalid {field} format. Please use 'YYYY-MM-DD-HH-MM'.")
            elif field == "dob":
                try:
                    dob = datetime.strptime(value, "%Y-%m-%d")  # Expecting the format 'YYYY-MM-DD'
                except ValueError:
                    raise ValueError(f"Invalid {field} format. Please use 'YYYY-MM-DD'.")
