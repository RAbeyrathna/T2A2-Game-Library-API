import functools

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.user_library import (
    User_library,
    user_library_schema,
    user_libraries_schema,
)
from models.library_item import (
    Library_item,
    library_item_schema,
    library_items_schema,
)
from models.game import Game

from controllers.auth_controller import is_user_admin

libraries_bp = Blueprint("cards", __name__, url_prefix="/library")


def has_library_permissions(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = int(get_jwt_identity())
        if "library_id" in kwargs:
            library_id = kwargs.get("library_id")
            stmt = db.select(User_library).filter_by(
                user_library_id=library_id
            )
            user_library = db.session.scalar(stmt)
        elif "library_item_id" in kwargs:
            library_item_id = kwargs.get("library_item_id")

            stmt = db.select(Library_item).filter_by(
                library_item_id=library_item_id
            )
            library_item = db.session.scalar(stmt)
            if library_item:
                stmt = db.select(User_library).filter_by(
                    user_library_id=library_item.user_library_id
                )
                user_library = db.session.scalar(stmt)
            else:
                return {
                    "error": f"Library item with ID '{library_item_id}' does not exist"
                }, 404

        is_admin = is_user_admin()
        if user_library and user_library.user_id == current_user_id:
            return fn(*args, **kwargs)
        elif is_admin:
            return fn(*args, **kwargs)
        else:
            return {"error": "User is not the owner of this library"}, 403

    return wrapper


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


# # http://localhost:8080/library/entry/all - GET
@libraries_bp.route("/entry/all")
def get_all_library_entries():
    stmt = db.select(Library_item)
    library_items = db.session.scalars(stmt)
    return library_items_schema.dump(library_items)


# # http://localhost:8080/library/entry/2 - GET
@libraries_bp.route("/entry/<int:library_item_id>")
def get_one_library_entry(library_item_id):  # library_item_id = 2
    stmt = db.select(Library_item).filter_by(
        library_item_id=library_item_id
    )  # select * from user_library where id=2
    library_item = db.session.scalar(stmt)
    if library_item:
        return library_item_schema.dump(library_item)
    else:
        return {
            "error": f"Library item with id {library_item_id} not found"
        }, 404


# http://localhost:8080/library/3 - POST
@libraries_bp.route("/<int:library_id>", methods=["POST"])
@jwt_required()
@has_library_permissions
def create_library_entry(library_id):
    body_data = library_item_schema.load(request.get_json())
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


@libraries_bp.route("/entry/<int:library_item_id>", methods=["DELETE"])
@jwt_required()
@has_library_permissions
def delete_library_item(library_item_id):
    # Query the library item to be deleted based on library_item_id
    stmt = db.select(Library_item).where(
        Library_item.library_item_id == library_item_id
    )
    library_entry = db.session.scalar(stmt)

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


@libraries_bp.route("/entry/<int:library_item_id>", methods=["PUT", "PATCH"])
@jwt_required()
@has_library_permissions
def update_library_item(library_item_id):
    # Get the JSON data from the request
    body_data = library_item_schema.load(request.get_json(), partial=True)

    # Query the library item to be patched
    stmt = db.select(Library_item).where(
        Library_item.library_item_id == library_item_id
    )
    library_entry = db.session.scalar(stmt)

    # Update the library item
    library_entry.status = body_data.get("status") or library_entry.status
    library_entry.score = body_data.get("score") or library_entry.score
    db.session.commit()
    return library_item_schema.dump(library_entry)
