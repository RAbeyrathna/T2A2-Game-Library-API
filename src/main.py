import os
from flask import Flask
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
