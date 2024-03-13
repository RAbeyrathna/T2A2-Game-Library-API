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

    @app.errorhandler(ValidationError)
    def validation_error(error):
        return {"error": error.messages}, 400

    @app.errorhandler(IntegrityError)
    def integrity_error(error):
        # Original error message from the database
        detail = str(error.orig)

        # Attempt to extract the key and value that caused the IntegrityError
        match = re.search(r"Key \((.*?)\)=\((.*?)\) already exists", detail)

        if match:
            key, value = match.groups()
            message = f"A record with the {key} '{value}' already exists."
        else:
            # If the pattern does not match, fall back to the original detail
            message = "A database constraint was violated."

        return {"error": message}, 409

    from controllers.cli_controllers import db_commands

    app.register_blueprint(db_commands)

    from controllers.auth_controller import auth_bp

    app.register_blueprint(auth_bp)

    from controllers.user_library_controller import libraries_bp

    app.register_blueprint(libraries_bp)

    from controllers.platform_controller import platforms_bp

    app.register_blueprint(platforms_bp)

    from controllers.genre_controller import genres_bp

    app.register_blueprint(genres_bp)

    from controllers.game_controller import games_bp

    app.register_blueprint(games_bp)

    return app
