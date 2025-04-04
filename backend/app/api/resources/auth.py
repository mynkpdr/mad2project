import os
from flask import render_template, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.api.api_models.auth import (
    auth_ns,
    login_model,
    signup_model,
    forgot_password_model,
)
from flask_restx import Resource
from app.models import OAuth, PasswordResetToken, Student, User
from app.extensions import db
from app.utils.custom import validate_fields
from app.utils.custom import generate_unique_username
from app.tasks import send_email_async
from werkzeug.exceptions import Conflict, Unauthorized, Forbidden, NotFound, BadRequest
import requests
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer

from app.api.resources.main import FileUtils
from app.utils.timezone import IndiaNow, IndiaTimeStampNow
from app.models.user import Status


@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_model, validate=True)
    def post(self):
        """
        Handle user login via email/password.
        """

        payload = auth_ns.payload
        email = payload.get("email")
        password = payload.get("password")

        validate_fields(
            [
                ("email", email, True),
                ("password", password, True),
            ]
        )

        user = User.query.filter_by(email=email).first()
        if not user:
            raise NotFound("User not found")
        if user and user.password is None:
            raise Unauthorized("Invalid email or password")

        if user and user.check_password(email, password):
            if not user.email_verified:
                raise Forbidden("Please verify your email address")
            if user.status and user.status == Status.SUSPENDED:
                raise Forbidden("Your account has been suspended")

            # If login successful, issue JWT token
            jwt_token = create_access_token(identity=str(user.id))
            response = {
                "message": "Login successful",
                "access_token": jwt_token,
                "user": {
                    "id": user.student_data.id if user.student_data else user.admin_data.id if user.admin_data else user.id,
                    "name": user.name,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role.value,
                    "profile_picture": user.profile_picture,
                },
            }
            user.last_login = IndiaTimeStampNow()
            db.session.commit()
            return response, 200
        raise Unauthorized("Invalid email or password")


@auth_ns.route("/signup")
class Signup(Resource):
    @auth_ns.expect(signup_model, validate=True)
    def post(self):
        """
        Register a new user
        """
        payload = auth_ns.payload
        email = payload.get("email")
        username = payload.get("username")
        password = payload.get("password")
        name = payload.get("name")
        phone_number = payload.get("phone_number", None)
        address = payload.get("address", None)
        gender = payload.get("gender", None)
        dob = payload.get("dob", None)
        profile_picture = payload.get("profile_picture", None)
        bio = payload.get("bio", None)
        qualification = payload.get("qualification", None)
        validate_fields(
            [
                ("email", email, True),
                ("username", username, False),
                ("password", password, True),
                ("name", name, True),
                ("phone_number", phone_number, False),
                ("address", address, False),
                ("gender", gender, False),
                ("dob", dob, False),
                ("profile_picture", profile_picture, False),
                ("bio", bio, False),
                ("qualification", qualification, False),
            ]
        )

        if User.query.filter_by(email=email).first():
            raise Conflict("User with this email already exists")
        if User.query.filter_by(username=username).first():
            raise Conflict("User with this username already exists")
        if not username:
            username = generate_unique_username()
        new_user = User(
            username=username,
            name=name,
            email=email,
            phone_number=phone_number,
            address=address,
            gender=gender,
            dob=dob,
            profile_picture=profile_picture,
            bio=bio,
            role="STUDENT",
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        new_student = Student(user_id=new_user.id, qualification=qualification)
        db.session.add(new_student)
        db.session.commit()
        # Generate email confirmation token
        try:
            serializer = URLSafeSerializer(os.getenv("SECRET_KEY"))
            email_confirmation_salt = os.getenv(
                "EMAIL_CONFIRMATION_SALT", "default-email-confirmation-salt"
            )
            token = serializer.dumps(email, salt=email_confirmation_salt)

            # Send confirmation email with the token
            confirm_url = f"{os.getenv('FRONTEND_URL')}/confirm-email/{token}"
            task = send_email_async.delay(
                to=email,
                subject="Confirm Your Email Address",
                body=f"Please use the following link to confirm your email address: {confirm_url}",
                html_body=render_template(
                    "confirm_email.html", confirm_url=confirm_url
                ),
            )
            return {
                "message": "Please check your email to confirm the account.", 'task_id': task.id
            }, 201
        except:
            raise BadRequest("An error occured while sending confirmation email")


@auth_ns.route("/confirm-email/<string:token>")
class ConfirmEmail(Resource):
    def get(self, token):
        """
        Confirm the user's email address.
        """
        try:

            serializer = URLSafeSerializer(os.getenv("SECRET_KEY"))
            email_confirmation_salt = os.getenv(
                "EMAIL_CONFIRMATION_SALT", "default-email-confirmation-salt"
            )
            # Verify the token and extract the email
            email = serializer.loads(
                token, salt=email_confirmation_salt
            )  # Token is valid for life :)
        except Exception:
            raise BadRequest("The confirmation link is either invalid or has expired")

        user = User.query.filter_by(email=email).first()
        if not user:
            raise NotFound("User not found")

        if user.email_verified:
            raise Conflict("Email already verified")

        # Mark the user as verified
        user.email_verified = True
        db.session.commit()

        # Send welcome email
        task = send_email_async.delay(
            to=email,
            subject="Welcome to ExamBhai",
            body=f"Welcome to ExamBhai",
            html_body=render_template("welcome_email.html", name=user.name),
        )
        return {"message": "Email confirmed successfully. You can now log in", 'task_id': task.id}, 200


@auth_ns.route("/login/google")
class GoogleLogin(Resource):
    @auth_ns.doc(False)
    def post(self):
        """
        Login the user with Google access token
        """
        # Extract access_token from the request
        access_token = auth_ns.payload.get("access_token")
        if not access_token:
            raise BadRequest("access_token is missing")
        # Validate the access_token
        token_info_url = "https://oauth2.googleapis.com/tokeninfo"
        token_info_response = requests.get(
            token_info_url, params={"access_token": access_token}
        )
        if token_info_response.status_code != 200:
            raise BadRequest("Invalid access token")
        token_info = token_info_response.json()
        # Verify token audience (client_id)
        client_id = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
        if token_info.get("aud") != client_id:
            return {"error": "Token audience does not match client ID"}, 401
        # Fetch user info using the access_token
        user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        user_info_response = requests.get(
            user_info_url, headers={"Authorization": f"Bearer {access_token}"}
        )
        if user_info_response.status_code != 200:
            return {"error": "Failed to fetch user info"}, 401
        user_info = user_info_response.json()
        email = user_info.get("email")
        name = user_info.get("name")
        profile_picture = user_info.get("picture")
        if profile_picture and "s96-c" in profile_picture:
            profile_picture = profile_picture.replace("s96-c", "s512-c")
        unique_id = user_info.get("sub")
        # Check if user exists, otherwise create
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            oauth_user = OAuth.query.filter_by(user_id=existing_user.id).first()
            if oauth_user:
                if oauth_user.platform != "google":
                    raise BadRequest(
                        "This email is registered in our database but isn't associated with your google account. Please use another method to login"
                    )
            else:
                new_oauth = OAuth(
                    user_id=existing_user.id, unique_id=unique_id, platform="google"
                )
                db.session.add(new_oauth)
                db.session.commit()
            if existing_user.status and existing_user.status.value.lower() == "suspended":
                raise Forbidden("Your account has been suspended")
            jwt_token = create_access_token(identity=str(existing_user.id))
            response = {
                "message": "Login successful",
                "access_token": jwt_token,
                "user": {
                    "id": existing_user.student_data.id if existing_user.student_data else existing_user.admin_data.id if existing_user.admin_data else existing_user.id,
                    "username": existing_user.username,
                    "name": existing_user.name,
                    "email": existing_user.email,
                    "role": existing_user.role.value,
                    "profile_picture": existing_user.profile_picture,
                },
            }
            existing_user.last_login = IndiaTimeStampNow()
            db.session.commit()
            return response, 200
        else:
            try:
                filename = FileUtils.get_unique_filename(f"{profile_picture}.jpg")
                filepath = os.path.join(
                    os.getenv("PROFILE_PICTURE_UPLOAD_FOLDER"), filename
                )
                profile_picture_response = requests.get(
                    profile_picture, stream=True
                )
                if profile_picture_response.status_code == 200:
                    with open(filepath, "wb") as f:
                        for chunk in profile_picture_response.iter_content(1024):
                            f.write(chunk)
                            profile_picture = filename
                else:
                    profile_picture = None
            except:
                profile_picture = None
            # Generate a unique username
            username = generate_unique_username()
            new_user = User(
                email=email,
                name=name,
                username=username,
                profile_picture=profile_picture,
                email_verified=True,
                role="STUDENT",
                last_login=IndiaTimeStampNow()
            )
            new_user.set_password(os.urandom(32).hex())  # Generate a secure random password
            db.session.add(new_user)
            new_student = Student(user=new_user)
            
            db.session.add(new_student)
            db.session.commit()
            new_oauth = OAuth(
                user_id=new_user.id,
                unique_id=unique_id,
                platform="google",
            )
            db.session.add(new_oauth)
            db.session.commit()
            jwt_token = create_access_token(identity=str(new_user.id))
            response = {
                "message": "Login successful",
                "access_token": jwt_token,
                "user": {
                    "id": new_student.id,
                    "name": new_user.name,
                    "email": new_user.email,
                    "username": new_user.username,
                    "role": new_user.role.value,
                    "profile_picture": new_user.profile_picture,
                },
            }
            return response, 200



@auth_ns.route("/login/facebook")
class FacebookLogin(Resource):
    @auth_ns.doc(False)
    def post(self):
        """
        Login the user with the facebook login
        """

        access_token = auth_ns.payload.get("facebookToken")
        if not access_token:
            raise BadRequest("access_token is missing")

        user_info_url = "https://graph.facebook.com/v10.0/me"
        user_info_params = {
            "fields": "id,name,email,picture.width(400).height(400)",  # Requesting necessary fields
            "access_token": access_token,
        }
        user_info_response = requests.get(user_info_url, params=user_info_params)
        if user_info_response.status_code != 200:
            raise Unauthorized("Facebook token is invalid")

        user_info = user_info_response.json()
        # Extract user details
        facebook_id = user_info.get("id")
        name = user_info.get("name", "Unknown")
        email = user_info.get("email")
        profile_picture = user_info.get("picture", {}).get("data", {}).get("url")

        # Check if user exists, otherwise create
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            oauth_user = OAuth.query.filter_by(user_id=existing_user.id).first()
            if oauth_user:
                if oauth_user.platform != "facebook":
                    raise BadRequest(
                        "This email is registered in our database but isn't associated with your facebook account. Please login with email and password"
                    )
            else:
                new_oauth = OAuth(
                    user_id=existing_user.id,
                    unique_id=facebook_id,
                    platform="facebook",
                )
                db.session.add(new_oauth)
                db.session.commit()
            if existing_user.status and existing_user.status.value.lower() == "suspended":
                raise Forbidden("Your account has been suspended")
            jwt_token = create_access_token(identity=str(existing_user.id))
            response = {
                "message": "Login successful",
                "access_token": jwt_token,
                "user": {
                    "id": existing_user.student_data.id if existing_user.student_data else existing_user.admin_data.id if existing_user.admin_data else existing_user.id,
                    "username": existing_user.username,
                    "name": existing_user.name,
                    "email": existing_user.email,
                    "role": existing_user.role.value,
                    "profile_picture": existing_user.profile_picture,
                },
            }
            existing_user.last_login = IndiaTimeStampNow()
            db.session.commit()
            return response, 200
        else:
            try:
                filename = FileUtils.get_unique_filename(f"{profile_picture}.jpg")
                filepath = os.path.join(
                    os.getenv("PROFILE_PICTURE_UPLOAD_FOLDER"), filename
                )

                profile_picture_response = requests.get(
                    profile_picture, stream=True
                )
                if profile_picture_response.status_code == 200:
                    with open(filepath, "wb") as f:
                        for chunk in profile_picture_response.iter_content(1024):
                            f.write(chunk)
                            profile_picture = filename
                else:
                    profile_picture = None
            except:
                profile_picture = None

            # Generate a unique username
            username = generate_unique_username()
            new_user = User(
                email=email,
                name=name,
                username=username,
                profile_picture=profile_picture,
                email_verified=True,
                role="STUDENT",
                last_login=IndiaTimeStampNow(),
            )
            new_user.set_password(os.urandom(32).hex())  # Generate a secure random password
            db.session.add(new_user)

            new_student = Student(user=new_user)
            
            db.session.add(new_student)
            db.session.commit()

            new_oauth = OAuth(
                user_id=new_user.id,
                unique_id=facebook_id,
                platform="facebook",
            )

            db.session.add(new_oauth)
            db.session.commit()

            jwt_token = create_access_token(identity=str(new_user.id))
            response = {
                "message": "Login successful",
                "access_token": jwt_token,
                "user": {
                    "id": new_student.id,
                    "name": new_user.name,
                    "email": new_user.email,
                    "username": new_user.username,
                    "role": new_user.role.value,
                    "profile_picture": new_user.profile_picture,
                },
            }
            return response, 200

@auth_ns.route("/forgot-password")
class ForgotPassword(Resource):
    @auth_ns.expect(forgot_password_model, validate=True)
    def post(self):
        """
        Handle password reset request.
        """

        request_data = auth_ns.payload
        email = request_data.get("email")

        validate_fields([("email", email, True)])
        user = User.query.filter_by(email=email).first()
        if not user:
            raise NotFound("No user found with this email address.")

        # Generate a reset token
        serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
        password_reset_salt = os.getenv(
            "PASSWORD_RESET_SALT", "default-password-reset-salt"
        )
        token = serializer.dumps(email, salt=password_reset_salt)

        # Send reset email
        reset_url = f"{os.getenv('FRONTEND_URL')}/reset-password/{token}"
        task = send_email_async.delay(
            to=email,
            subject="Password Reset Request",
            body=f"Please use the following link to reset your password: {reset_url}",
            html_body=render_template("reset_password.html", reset_url=reset_url),
        )
        storeToken = PasswordResetToken(token=token)
        db.session.add(storeToken)
        db.session.commit()
        return {
            "message": "Password reset instructions have been sent to your email.", 'task_id': task.id
        }, 200

@auth_ns.route('/reset-password')
class ResetPassword(Resource):
    @jwt_required()
    def post(self):
        """
        Reset the user's password.
        """
        user = User.query.filter_by(id=get_jwt_identity()).first()
        current_password = auth_ns.payload.get("current_password")
        new_password = auth_ns.payload.get("new_password")
        validate_fields(
            [
                ("current_password", current_password, True),
                ("new_password", new_password, True),
            ]
        )
        if current_password == new_password:
            raise Conflict("New password cannot be same as old password")
        if not user.check_password(user.email, current_password):
            raise BadRequest("Invalid current password")
        user.set_password(new_password)
        db.session.commit()
        not_me_url = f"{os.getenv('FRONTEND_URL')}/forgot-password"
        task = send_email_async.delay(
            to=user.email,
            subject="Password changed",
            body=f"Did you change your password?",
            html_body=render_template("reset_password_successful.html", not_me_url=not_me_url, reset_date=IndiaNow().strftime("%A, %d %B %Y, %I:%M:%S %p %Z")),
        )
        return {"message": "Password has been reset successfully.", "task_id": task.id}, 200
    
@auth_ns.route("/reset-password/<string:token>")
class ResetPasswordWithToken(Resource):
    def post(self, token):
        """
        Reset the user's password.
        """
        reset_token = PasswordResetToken.query.filter_by(token=token).first()
        if not reset_token:
            raise BadRequest("Invalid reset token")
        if reset_token and reset_token.used:
            raise BadRequest("Password has already been reset using this token")

        password_reset_salt = os.getenv(
            "PASSWORD_RESET_SALT", "default-password-reset-salt"
        )
        serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
        try:
            # Verify the token and extract the email
            email = serializer.loads(
                token, salt=password_reset_salt, max_age=3600
            )  # Token is valid for 1 hour
        except Exception:
            raise BadRequest("The reset link is either invalid or has expired.")

        # Parse the new password from the request
        request_data = auth_ns.payload
        new_password = request_data.get("new_password")
        if not new_password:
            raise BadRequest("New password is required")

        user = User.query.filter_by(email=email).first()
        if not user:
            raise BadRequest("User not found")
        if user and user.check_password(user.email, new_password):
            raise Conflict("New password cannot be same as old password")
        # Set the new password
        user.set_password(new_password)
        if not user.email_verified:
            user.email_verified = True
        if reset_token:
            reset_token.used = True  # Set as used
        db.session.commit()
        not_me_url = f"{os.getenv('FRONTEND_URL')}/forgot-password"
        task = send_email_async.delay(
            to=user.email,
            subject="Password changed",
            body=f"Did you change your password?",
            html_body=render_template("reset_password_successful.html", not_me_url=not_me_url, reset_date=IndiaNow().strftime("%A, %d %B %Y, %I:%M:%S %p %Z")),
        )
        return {"message": "Your password has been reset successfully", 'task_id': task.id}, 200


@auth_ns.route("/validate-email")
class CheckEmail(Resource):
    def post(self):
        """
        Check if the email is already registered.
        """
        data = auth_ns.payload
        email = data.get("email")

        validate_fields([("email", email, True)])

        # Check if the email already exists in the database
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise Conflict("This email is already registered.")

        return {"message": "This email is available."}, 200  # Email is available
