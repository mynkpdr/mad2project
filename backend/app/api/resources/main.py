import time
import os
import uuid

from flask_jwt_extended import jwt_required
from werkzeug.datastructures.file_storage import FileStorage
from app.api.api_models.main import main_ns
from flask_restx import Resource
from app.config import DevelopmentConfig
from werkzeug.exceptions import BadRequest

upload_parser = main_ns.parser()
upload_parser.add_argument("file", location="files", type=FileStorage, required=True)
upload_parser.add_argument("type", type=str, required=True, help="Type of the file")


class FileUtils:
    @staticmethod
    def allowed_file_image(filename):
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower()
            in DevelopmentConfig.ALLOWED_EXTENSIONS_IMAGE
        )

    @staticmethod
    def get_unique_filename(filename):
        ext = filename.rsplit(".", 1)[1].lower()
        unique_name = str(int(time.time())) + "_" + str(uuid.uuid4()) + "." + ext
        return unique_name

    @staticmethod
    def is_file_size_allowed(file):
        file.seek(0, 2)  # Move the cursor to the end of the file
        file_size = file.tell()
        file.seek(0)  # Reset the cursor to the beginning of the file
        return file_size <= DevelopmentConfig.MAX_FILE_SIZE


@main_ns.route("/upload")
@main_ns.expect(upload_parser)
class Upload(Resource):
    @jwt_required()
    def post(self):
        """Upload a file"""
        args = upload_parser.parse_args()
        file_type = args["type"]  # File type from request
        image = args["file"]  # Image file from request.files
        if not file_type or file_type not in ["profile_picture", "question_image"]:
            raise BadRequest("Invalid image type")

        if image and FileUtils.allowed_file_image(image.filename):
            if FileUtils.is_file_size_allowed(image):
                filename = FileUtils.get_unique_filename(
                    image.filename
                )  # Secure the filename
                if file_type == "profile_picture":
                    filepath = os.path.join(
                        os.getenv("PROFILE_PICTURE_UPLOAD_FOLDER"), filename
                    )
                elif file_type == "question_image":
                    filepath = os.path.join(
                        os.getenv("QUESTION_IMAGE_UPLOAD_FOLDER"), filename
                    )
                image.save(filepath)
                return {
                    "success": True,
                    "message": "Image uploaded successfully",
                    "filename": filename,
                }, 201
            else:
                raise BadRequest("The image should be under 1 MB")
        else:
            raise BadRequest("Invalid file type")
