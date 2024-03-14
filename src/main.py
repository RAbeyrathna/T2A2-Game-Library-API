import os
import re

from flask import Flask
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

from init import db, ma, bcrypt, jwt


def create_app():
    app = Flask(__name__)

    app.json.sort_keys = False

    # Configs
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    # Connect libraries with flask app
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.errorhandler(400)
    def attribute_error(error):
        return {"error": str(error)}, 400

    @app.errorhandler(400)
    def bad_request(error):
        return {"error": str(error)}, 400

    @app.errorhandler(404)
    def not_found(error):
        return {"error": str(error)}, 404

    @app.errorhandler(500)
    def internal_server(error):
        return {"error": str(error)}, 500

    @app.errorhandler(ValidationError)
    def validation_error(error):
        return {"error": error.messages}, 400

    @app.errorhandler(IntegrityError)
    def integrity_error_handler(error):
        # Original error message from the database
        error_detail = str(error.orig)

        # Check for 'DETAIL:' part in the error message
        detail_start_index = error_detail.find("DETAIL:") + len("DETAIL:")
        detail_msg = (
            error_detail[detail_start_index:].strip()
            if detail_start_index > -1
            else ""
        )

        # Extract meaningful message from detail
        message = "A database constraint was violated."
        if "is not present in table" in detail_msg:
            # Extract the value and table name
            extracted_values = detail_msg.split("Key ")[1].split(
                " is not present in table"
            )[0]
            parts = extracted_values.split(")=(")
            field_name = parts[0][1:]
            field_value = parts[1][:-1]
            table_name = detail_msg.split("is not present in table ")[1].split(
                '"'
            )[1]
            message = f"{field_name.capitalize()} with the value '{field_value}' does not exist in the '{table_name.capitalize()}' table."

        elif "already exists" in detail_msg:
            # Extract the key-value pair that already exists
            key_value_pair = detail_msg.split("already exists.")[0]
            message = f"A record with the {key_value_pair} already exists."

        return {"error": message}, 409

    from controllers.cli_controllers import db_commands

    app.register_blueprint(db_commands)

    from controllers.auth_controller import auth_bp

    app.register_blueprint(auth_bp)

    from controllers.users_controller import user_bp

    app.register_blueprint(user_bp)

    from controllers.user_library_controller import libraries_bp

    app.register_blueprint(libraries_bp)

    from controllers.platform_controller import platforms_bp

    app.register_blueprint(platforms_bp)

    from controllers.genre_controller import genres_bp

    app.register_blueprint(genres_bp)

    from controllers.game_controller import games_bp

    app.register_blueprint(games_bp)

    return app


message = "(genre) with id "
