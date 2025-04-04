from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from werkzeug.exceptions import Forbidden, NotFound, Unauthorized
from app.models.user import Role, User

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception:
            raise Unauthorized("Missing Authorization Header")

        # Now that the JWT has been verified, get the identity (user id)
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if not current_user:
            raise NotFound("User not found!")

        if current_user.role != Role.ADMIN: # Check if the user is an admin !!! IMPORTANT
            raise Forbidden("You do not have the required permissions to access this resource.")

        # Everything is fine, proceed with the decorated function
        return f(*args, **kwargs)

    return decorated_function
