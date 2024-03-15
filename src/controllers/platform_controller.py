from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from init import db
from models.platform import Platform, platform_schema, platforms_schema
from models.game_platform import Game_platform, game_platform_schema
from models.game import Game

from controllers.auth_controller import authorise_as_admin

platforms_bp = Blueprint("platforms", __name__, url_prefix="/platforms")


# Route to get all platforms from the database
# # http://localhost:8080/platforms - GET
@platforms_bp.route("/")
def get_all_platforms():

    # SELECT * FROM platforms;
    stmt = db.select(Platform)
    platforms = db.session.scalars(stmt)

    # Return all platform records in database
    return platforms_schema.dump(platforms)


# Route to get an individual platform from the database
# # http://localhost:8080/platforms/1 - GET
# Assume platform_id = 1
@platforms_bp.route("/<int:platform_id>")
def get_one_platform(platform_id):

    # SELECT * FROM platforms WHERE platform_id = 1;
    stmt = db.select(Platform).filter_by(platform_id=platform_id)
    platform = db.session.scalar(stmt)

    # If platform record exists, return to user
    if platform:
        return platform_schema.dump(platform)

    # Else return error that platform was not found
    else:
        return {"error": f"Platform with id {platform_id} not found"}, 404


# Route to get create a platform in the database
# http://localhost:8080/platforms - POST
@platforms_bp.route("/", methods=["POST"])
@jwt_required()
# User must be an admin to use this function
@authorise_as_admin  # # is_admin = True
def create_platform():

    # Get the platform data from the body of the request
    body_data = platform_schema.load(request.get_json())

    # Create a new platform model instance
    platform = Platform(
        platform_name=body_data.get("platform_name"),
        platform_type=body_data.get("platform_type"),
    )

    # Add platform to the session and commit
    db.session.add(platform)
    db.session.commit()

    # Return the newly created platform
    return platform_schema.dump(platform), 201


# Route to get delete a platform from the database
# http://localhost:8080/platforms/3 - DELETE
# Assume platform_id = 3
@platforms_bp.route("/<int:platform_id>", methods=["DELETE"])
@jwt_required()
@authorise_as_admin  # is_admin = True
def delete_platform(platform_id):

    # SELECT * FROM platforms WHERE platform_id = 3;
    stmt = db.select(Platform).where(Platform.platform_id == platform_id)
    platform = db.session.scalar(stmt)

    # If platform record exists, delete the platform and commit
    if platform:
        db.session.delete(platform)
        db.session.commit()

        return {
            "message": f"Platform '{platform.platform_name}' has been deleted successfully"
        }
    # Else, return error message
    else:
        return {"error": f"Platform with id {platform_id} not found"}, 404


# Route to get update a platform from the database
# http://localhost:8080/platforms/5 - PUT, PATCH
# Assume platform_id = 5
@platforms_bp.route("/<int:platform_id>", methods=["PUT", "PATCH"])
@jwt_required()
@authorise_as_admin  # is_admin = True
def update_platform(platform_id):

    # Get the platform data to be updated from the body of the request
    body_data = platform_schema.load(request.get_json(), partial=True)

    # SELECT * FROM platforms WHERE platform_id = 5;
    stmt = db.select(Platform).filter_by(platform_id=platform_id)
    platform = db.session.scalar(stmt)

    # If platform record exists, update the fields specified
    if platform:
        platform.platform_name = (
            body_data.get("platform_name") or platform.platform_name
        )
        platform.platform_type = (
            body_data.get("platform_type") or platform.platform_type
        )

        # Commit the changes and return the updated platform back
        db.session.commit()
        return platform_schema.dump(platform)

    # Else, return an error message
    else:
        return {"error": f"Platform with id {platform_id} not found"}, 404


# Route to assign a platform to a game
# http://localhost:8080/platforms/1/game/2 - POST
# Assume platform_id = 1 and game_id = 2
@platforms_bp.route("/<int:platform_id>/game/<int:game_id>", methods=["POST"])
@jwt_required()
@authorise_as_admin  # is_admin = True
def assign_game_platform(platform_id, game_id):

    # Create a new game_platform model instance
    game_platform = Game_platform(game_id=game_id, platform_id=platform_id)

    # Add that to the session and commit
    db.session.add(game_platform)
    db.session.commit()

    # Return the newly assigned platform and game
    return game_platform_schema.dump(game_platform), 201


# Route to delete a platform from a game
# http://localhost:8080/platforms/1/game/2 - DELETE
# Assume platform_id = 1 and game_id = 2
@platforms_bp.route(
    "/<int:platform_id>/game/<int:game_id>", methods=["DELETE"]
)
@jwt_required()
@authorise_as_admin  # is_admin = True
def delete_game_platform(platform_id, game_id):

    # SELECT * FROM game_platforms WHERE platform_id = 1 AND game_id = 2;
    stmt = db.select(Game_platform).where(
        Game_platform.platform_id == platform_id
        and Game_platform.game_id == game_id
    )
    game_platform = db.session.scalar(stmt)

    # Get game record with same game_id to use in return message
    # SELECT * FROM games WHERE game_id = 1;
    stmt = db.select(Game).where(Game.game_id == game_id)
    game = db.session.scalar(stmt)

    # Get platform record with same platform_id to use in return message
    # SELECT * FROM platforms WHERE platform_id = 2;
    stmt = db.select(Platform).where(Platform.platform_id == platform_id)
    platform = db.session.scalar(stmt)

    # If game_platform record exists, delete it from the session and commit
    if game_platform:
        db.session.delete(game_platform)
        db.session.commit()
        return {
            "message": f"Platform '{platform.platform_name}' has been successfully deleted from the game '{game.game_title}'"
        }

    # Else return message that platform is not assigned to specified game
    else:
        return {
            "error": f"Platform '{platform.platform_name}' is not assigned to the game '{game.game_title}'"
        }, 404
