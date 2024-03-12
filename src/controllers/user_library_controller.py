from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.user_library import (
    User_library,
    user_library_schema,
    user_libraries_schema,
)
from models.library_item import Library_item, library_item_schema
from models.game import Game

from controllers.auth_controller import is_user_admin

libraries_bp = Blueprint("cards", __name__, url_prefix="/library")


# # http://localhost:8080/library/all - GET
@libraries_bp.route("/all")
def get_all_libraries():
    stmt = db.select(User_library)
    libraries = db.session.scalars(stmt)
    return user_libraries_schema.dump(libraries)


# # http://localhost:8080/library/2 - GET
@libraries_bp.route("/<int:library_id>")
def get_one_library(library_id):  # library_id = 2
    stmt = db.select(User_library).filter_by(
        user_library_id=library_id
    )  # select * from user_library where id=2
    user_library = db.session.scalar(stmt)
    if user_library:
        return user_library_schema.dump(user_library)
    else:
        return {"error": f"User Library with id {library_id} not found"}, 404


# http://localhost:8080/library/3 - POST
@libraries_bp.route("/<int:library_id>", methods=["POST"])
@jwt_required()
def create_library_entry(library_id):
    # Check if user owns the library
    is_library_owner = check_library_owner(library_id)
    is_admin = is_user_admin()
    if not is_library_owner and not is_admin:
        return {"error": "User is not the owner of this library"}, 403
    body_data = request.get_json()
    # Create a new library_item model instance
    library_entry = Library_item(
        user_library_id=library_id,
        game_id=body_data.get("game_id"),
        status=body_data.get("status"),
        score=body_data.get("score"),
    )
    # Add that to the session and commit
    db.session.add(library_entry)
    db.session.commit()
    # return the newly created library_item
    return library_item_schema.dump(library_entry), 201


@libraries_bp.route("/<int:library_item_id>", methods=["DELETE"])
@jwt_required()
def delete_library_item(library_item_id):
    # Query the library item to be deleted based on library_item_id
    stmt = db.select(Library_item).where(
        Library_item.library_item_id == library_item_id
    )
    library_entry = db.session.scalar(stmt)

    if library_entry:
        # Check if user owns the library item
        is_library_owner = check_library_owner(library_entry.user_library_id)
        is_admin = is_user_admin()
        if not is_library_owner and not is_admin:
            return {
                "error": "User is not the owner of this library entry"
            }, 403

        # Get game title for user message before deleting the library entry
        stmt = db.select(Game).where(Game.game_id == library_entry.game_id)
        game = db.session.scalar(stmt)
        game_title = game.game_title

        # Delete the library item
        db.session.delete(library_entry)
        db.session.commit()

        return {
            "message": f"Game '{game_title}' has been deleted from your library successfully"
        }
    else:
        return {
            "error": f"Library item with ID {library_item_id} does not exist in your library"
        }, 404


@libraries_bp.route("/<int:library_item_id>", methods=["PUT", "PATCH"])
@jwt_required()
def patch_library_item(library_item_id):
    # Get the JSON data from the request
    body_data = request.get_json()

    # Query the library item to be patched
    stmt = db.select(Library_item).where(
        Library_item.library_item_id == library_item_id
    )
    library_entry = db.session.scalar(stmt)

    if library_entry:
        # Check if user owns the library item
        is_library_owner = check_library_owner(library_entry.user_library_id)
        is_admin = is_user_admin()
        if not is_library_owner and not is_admin:
            return {
                "error": "User is not the owner of this library entry"
            }, 403

        # Update the library item
        library_entry.status = body_data.get("status") or library_entry.status
        library_entry.score = body_data.get("score") or library_entry.score
        db.session.commit()

        return library_item_schema.dump(library_entry)
    else:
        return {
            "error": f"Library item with ID {library_item_id} does not exist"
        }, 404


def check_library_owner(library_id):
    current_user_id = int(get_jwt_identity())
    stmt = db.select(User_library).filter_by(user_library_id=library_id)
    user_library = db.session.scalar(stmt)
    if user_library and user_library.user_id == current_user_id:
        return True
    else:
        return False


# # Delete library item using library_id and game_id in route
# @libraries_bp.route("/<int:library_id>/<int:game_id>", methods=["DELETE"])
# @jwt_required()
# def delete_library_item(library_id, game_id):
#     # Check if user owns the library
#     is_library_owner = check_library_owner(library_id)
#     if not is_library_owner:
#         return {"error": "User is not the owner of this library"}, 403

#     # Query the library item to be deleted
#     stmt = db.select(Library_item).where(
#         Library_item.user_library_id == library_id,
#         Library_item.game_id == game_id,
#     )
#     library_entry = db.session.scalar(stmt)

#     # Get game title for user message
#     stmt = db.select(Game).where(Game.game_id == game_id)
#     game = db.session.scalar(stmt)
#     game_title = game.game_title

#     if library_entry:
#         # Delete the library item
#         db.session.delete(library_entry)
#         db.session.commit()

#         return {
#             "message": f"Game '{game_title}' has been deleted from your library successfully"
#         }
#     else:
#         return {
#             "error": f"Game with ID {game_id} does not exist in your library"
#         }, 404
