from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.platform import Platform, platform_schema, platforms_schema
from models.game_platform import Game_platform, game_platform_schema
from models.game import Game

from controllers.auth_controller import is_user_admin

platforms_bp = Blueprint("platforms", __name__, url_prefix="/platforms")


@platforms_bp.route("/")
def get_all_platforms():
    stmt = db.select(Platform)
    platforms = db.session.scalars(stmt)
    return platforms_schema.dump(platforms)


# # http://localhost:8080/platforms/1 - GET
@platforms_bp.route("/<int:platform_id>")
def get_one_platform(platform_id):  # platform_id = 1
    stmt = db.select(Platform).filter_by(
        platform_id=platform_id
    )  # select * from platforms where platform_id=2
    platform = db.session.scalar(stmt)
    if platform:
        return platform_schema.dump(platform)
    else:
        return {"error": f"Platform with id {platform_id} not found"}, 404


# http://localhost:8080/platforms - POST
@platforms_bp.route("/", methods=["POST"])
@jwt_required()
def create_platform():
    # Check if user is an admin
    is_admin = is_user_admin()
    if not is_admin:
        return {"error": "User is not authorised to create a platform"}, 403
    body_data = platform_schema.load(request.get_json())
    # Create a new platform model instance
    platform = Platform(
        platform_name=body_data.get("platform_name"),
        platform_type=body_data.get("platform_type"),
    )
    # Add that to the session and commit
    db.session.add(platform)
    db.session.commit()
    # return the newly created platform
    return platform_schema.dump(platform), 201


# http://localhost:8080/platforms/3 - DELETE
@platforms_bp.route("/<int:platform_id>", methods=["DELETE"])
@jwt_required()
def delete_platform(platform_id):
    # Check if user is an admin
    is_admin = is_user_admin()
    if not is_admin:
        return {"error": "User is not authorised to delete a platform"}, 403
    # get the platform from the db with platform_id = platform_id
    stmt = db.select(Platform).where(Platform.platform_id == platform_id)
    platform = db.session.scalar(stmt)
    # if platform exists
    if platform:
        # delete the playform from the session and commit
        db.session.delete(platform)
        db.session.commit()
        # return msg
        return {
            "message": f"Platform '{platform.platform_name}' has been deleted successfully"
        }
    # else
    else:
        # return error msg
        return {"error": f"Platform with id {platform_id} not found"}, 404


# http://localhost:8080/platforms/5 - PUT, PATCH
@platforms_bp.route("/<int:platform_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_platform(platform_id):
    # Check if user is an admin
    is_admin = is_user_admin()
    if not is_admin:
        return {"error": "User is not authorised to edit a platform"}, 403
    # Get the data to be updated from the body of the request
    body_data = platform_schema.load(request.get_json(), partial=True)
    # get the platform from the db whose fields need to be updated
    stmt = db.select(Platform).filter_by(platform_id=platform_id)
    platform = db.session.scalar(stmt)
    # if platform exists
    if platform:
        # update the fields
        platform.platform_name = (
            body_data.get("platform_name") or platform.platform_name
        )
        platform.platform_type = (
            body_data.get("platform_type") or platform.platform_type
        )
        # commit the changes
        db.session.commit()
        # return the updated platform back
        return platform_schema.dump(platform)
    # else
    else:
        # return error msg
        return {"error": f"Platform with id {platform_id} not found"}, 404


# http://localhost:8080/platforms/4/game/1 - POST
@platforms_bp.route("/<int:platform_id>/game/<int:game_id>", methods=["POST"])
@jwt_required()
def assign_game_platform(platform_id, game_id):
    # Check if user is an admin
    is_admin = is_user_admin()
    if not is_admin:
        return {
            "error": "User is not authorised to assign a platform to a game"
        }, 403
    # Create a new game_platform model instance
    game_platform = Game_platform(game_id=game_id, platform_id=platform_id)
    # Add that to the session and commit
    db.session.add(game_platform)
    db.session.commit()
    # return the newly assigned platform
    return game_platform_schema.dump(game_platform), 201


# http://localhost:8080/platforms/6/game/2 - DELETE
@platforms_bp.route(
    "/<int:platform_id>/game/<int:game_id>", methods=["DELETE"]
)
@jwt_required()
def delete_game_platform(platform_id, game_id):
    # Check if user is an admin
    is_admin = is_user_admin()
    if not is_admin:
        return {
            "error": "User is not authorised to delete a platform from a game"
        }, 403
    # get the platform from the db with platform_id = platform_id
    stmt = db.select(Game_platform).where(
        Game_platform.platform_id == platform_id
        and Game_platform.game_id == game_id
    )
    game_platform = db.session.scalar(stmt)
    stmt = db.select(Game).where(Game.game_id == game_id)
    game = db.session.scalar(stmt)
    stmt = db.select(Platform).where(Platform.platform_id == platform_id)
    platform = db.session.scalar(stmt)
    # if game_platform exists
    if game_platform:
        # delete the game_platform from the session and commit
        db.session.delete(game_platform)
        db.session.commit()
        # return msg

        return {
            "message": f"Platform '{platform.platform_name}' has been successfully deleted from the game '{game.game_title}'"
        }
    # else
    else:
        # return error msg
        return {
            "error": f"Platform '{platform.platform_name}' is not assigned to the game '{game.game_title}'"
        }, 404
