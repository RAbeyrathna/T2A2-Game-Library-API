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


# Decorator function to check if user has permissions to modify a library or library item
def has_library_permissions(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):

        # Get current logged in user with JWT torken
        current_user_id = int(get_jwt_identity())

        # If route is using library_id route, get the library_id
        if "library_id" in kwargs:
            library_id = kwargs.get("library_id")

            # SELECT * FROM user_library WHERE user_library_id = route_library_id;
            stmt = db.select(User_library).filter_by(
                user_library_id=library_id
            )
            user_library = db.session.scalar(stmt)

        # If route is using library_item_id route, get the library_item_id
        elif "library_item_id" in kwargs:
            library_item_id = kwargs.get("library_item_id")

            # SELECT * FROM library_item WHERE library_item_id = route_library_item_id;
            stmt = db.select(Library_item).filter_by(
                library_item_id=library_item_id
            )
            library_item = db.session.scalar(stmt)

            # If library_item record exists, get the associated User_library record
            if library_item:

                # SELECT * FROM user_library WHERE user_library_id = library_item.user_library_id;
                stmt = db.select(User_library).filter_by(
                    user_library_id=library_item.user_library_id
                )
                user_library = db.session.scalar(stmt)
            # Else, return error that library_item_id was not found in DB
            else:
                return {
                    "error": f"Library item with ID '{library_item_id}' does not exist"
                }, 404

        # Run check if user is an admin (does not need to be library or item owner)
        is_admin = is_user_admin()

        # If user_library record exists AND the user is the library owner OR an admin
        if user_library and (
            user_library.user_id == current_user_id or is_admin
        ):
            # Continue running the decorated function
            return fn(*args, **kwargs)

        # Else, return error that user does not have permission
        else:
            return {"error": "User is not the owner of this library"}, 403

    return wrapper


# Route to get all libraries in the database
# # http://localhost:8080/library/all - GET
@libraries_bp.route("/all")
def get_all_libraries():

    # SELECT * FROM user_library;
    stmt = db.select(User_library)
    libraries = db.session.scalars(stmt)

    # Return all User_library records in database
    return user_libraries_schema.dump(libraries)


# Route to get an individual library from the database
# # http://localhost:8080/library/2 - GET
# Assume library_id = 2
@libraries_bp.route("/<int:library_id>")
def get_one_library(library_id):

    # SELECT * FROM user_library WHERE user_library_id = 2;
    stmt = db.select(User_library).filter_by(user_library_id=library_id)
    user_library = db.session.scalar(stmt)

    # If user_library record exists, return to user
    if user_library:
        return user_library_schema.dump(user_library)

    # Else return error that the user_library was not found
    else:
        return {"error": f"User Library with id {library_id} not found"}, 404


# Route to get all library entries in the database
# # http://localhost:8080/library/entry/all - GET
@libraries_bp.route("/entry/all")
def get_all_library_entries():

    # SELECT * FROM library_items;
    stmt = db.select(Library_item)
    library_items = db.session.scalars(stmt)

    # Return all library_item records in database
    return library_items_schema.dump(library_items)


# Route to get an individual library item from the database
# # http://localhost:8080/library/entry/1 - GET
# Assume library_id = 1
@libraries_bp.route("/entry/<int:library_item_id>")
def get_one_library_entry(library_item_id):

    # SELECT * FROM library_items WHERE library_item_id = 1;
    stmt = db.select(Library_item).filter_by(library_item_id=library_item_id)
    library_item = db.session.scalar(stmt)

    # If library_item record exists, return to user
    if library_item:
        return library_item_schema.dump(library_item)

    # Else return error that the library_item record was not found
    else:
        return {
            "error": f"Library item with id {library_item_id} not found"
        }, 404


# Route to get create a library entry into a library
# http://localhost:8080/library/3 - POST
@libraries_bp.route("/<int:library_id>", methods=["POST"])
@jwt_required()
# Account must be an admin or the owner of the specified library
@has_library_permissions
def create_library_entry(library_id):

    # Get the library_item data from the body of the request
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

    # Return the newly created library_item
    return library_item_schema.dump(library_entry), 201


# Route to get delete a library entry from a library
# http://localhost:8080/library/entry/3 - POST
# Assume library_item_id = 3
@libraries_bp.route("/entry/<int:library_item_id>", methods=["DELETE"])
@jwt_required()
# Account must be an admin or the owner of the specified library
@has_library_permissions
def delete_library_item(library_item_id):

    # Query the library item to be deleted based on library_item_id
    # SELECT * FROM library_items WHERE library_item_id = 3;
    stmt = db.select(Library_item).where(
        Library_item.library_item_id == library_item_id
    )
    library_entry = db.session.scalar(stmt)

    # Get game title for user message before deleting the library entry
    # SELECT * FROM games WHERE game_id = library_entry.game_id;
    stmt = db.select(Game).where(Game.game_id == library_entry.game_id)
    game = db.session.scalar(stmt)
    game_title = game.game_title

    # Delete the library item and commit
    db.session.delete(library_entry)
    db.session.commit()

    # Return message specifying what game was deleted from the library
    return {
        "message": f"Game '{game_title}' with library_item_id {library_item_id} has been deleted from your library successfully"
    }


# Route to get update a library entry from a library
# http://localhost:8080/library/entry/3 - POST
@libraries_bp.route("/entry/<int:library_item_id>", methods=["PUT", "PATCH"])
@jwt_required()
# Account must be an admin or the owner of the specified library
@has_library_permissions
def update_library_item(library_item_id):

    # Get the library_item data to be updated from the body of the request
    body_data = library_item_schema.load(request.get_json(), partial=True)

    # SELECT * FROM library_items WHERE library_item_id = 3;
    stmt = db.select(Library_item).where(
        Library_item.library_item_id == library_item_id
    )
    library_entry = db.session.scalar(stmt)

    # Update the library item fields and commit
    library_entry.status = body_data.get("status") or library_entry.status
    library_entry.score = body_data.get("score") or library_entry.score

    db.session.commit()

    # Return the updated library item to the user
    return library_item_schema.dump(library_entry)
