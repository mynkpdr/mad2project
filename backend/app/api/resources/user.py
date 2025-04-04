from flask_restx import Resource
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.api_models.user import user_ns
from flask_jwt_extended import create_access_token
from app.extensions import db
from werkzeug.exceptions import BadRequest
@user_ns.route("/user_token")
class UserToken(Resource):
    @jwt_required()
    def post(self):
        user = User.query.get(get_jwt_identity())
        token = create_access_token(
            identity={
                "id": user.id,
                "name": user.name,
                "username": user.username,
                "email": user.email,
                "role": user.role.value,
                "profile_picture": user.profile_picture,
            }
        )
        return token, 200

@user_ns.route("/notifications")
class UserNotifications(Resource):
    @jwt_required()
    def get(self):
        user = User.query.get(get_jwt_identity())
        return {"notifications_enabled": user.notifications}, 200

@user_ns.route("/notifications/<string:toggle>")
class UserNotificationsToggle(Resource):
    @jwt_required()
    def post(self, toggle):
        user = User.query.get(get_jwt_identity())
        if not toggle in ["enable", "disable"]:
            raise BadRequest("Invalid toggle value")
        if toggle == "enable":
            user.notifications = True
        elif toggle == "disable":
            user.notifications = False
        db.session.commit()
        return {"notifications_enabled": user.notifications}, 200
