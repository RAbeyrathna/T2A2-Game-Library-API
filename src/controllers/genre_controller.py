from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.genre import Genre, genre_schema, genres_schema
from models.game_genre import Game_genre, game_genre_schema
from models.game import Game

from controllers.auth_controller import is_user_admin

genres_bp = Blueprint("genres", __name__, url_prefix="/genres")


# # http://localhost:8080/genres - GET
@genres_bp.route("/")
def get_all_genres():
    stmt = db.select(Genre)
    genres = db.session.scalars(stmt)
    return genres_schema.dump(genres)


# # http://localhost:8080/genres/1 - GET
@genres_bp.route("/<int:genre_id>")
def get_one_genre(genre_id):  # genre_id = 1
    stmt = db.select(Genre).filter_by(
        genre_id=genre_id
    )  # select * from genres where genre_id = 1
    genre = db.session.scalar(stmt)
    if genre:
        return genre_schema.dump(genre)
    else:
        return {"error": f"Genre with id {genre_id} not found"}, 404


# http://localhost:8080/genres - POST
@genres_bp.route("/", methods=["POST"])
@jwt_required()
def create_genre():
    # Check if user is an admin
    is_admin = is_user_admin()
    if not is_admin:
        return {"error": "User is not authorised to create a genre"}, 403
    body_data = request.get_json()
    # Create a new genre model instance
    genre = Genre(genre_name=body_data.get("genre_name"))
    # Add that to the session and commit
    db.session.add(genre)
    db.session.commit()
    # return the newly created genre
    return genre_schema.dump(genre), 201


# http://localhost:8080/genres/6 - DELETE
@genres_bp.route("/<int:genre_id>", methods=["DELETE"])
@jwt_required()
def delete_genre(genre_id):
    # Check if user is an admin
    is_admin = is_user_admin()
    if not is_admin:
        return {"error": "User is not authorised to delete a genre"}, 403
    # get the genre from the db with genre_id = genre_id
    stmt = db.select(Genre).where(Genre.genre_id == genre_id)
    genre = db.session.scalar(stmt)
    # if card exists
    if genre:
        # delete the genre from the session and commit
        db.session.delete(genre)
        db.session.commit()
        # return msg
        return {
            "message": f"Genre '{genre.genre_name}' has been deleted successfully"
        }
    # else
    else:
        # return error msg
        return {"error": f"Genre with id {genre_id} not found"}, 404


# http://localhost:8080/genres/5 - PUT, PATCH
@genres_bp.route("/<int:genre_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_genre(genre_id):
    # Check if user is an admin
    is_admin = is_user_admin()
    if not is_admin:
        return {"error": "User is not authorised to edit a genre"}, 403
    # Get the data to be updated from the body of the request
    body_data = request.get_json()
    # get the card from the db whose fields need to be updated
    stmt = db.select(Genre).filter_by(genre_id=genre_id)
    genre = db.session.scalar(stmt)
    # if genre exists
    if genre:
        # update the fields
        genre.genre_name = body_data.get("genre_name") or genre.genre_name
        # commit the changes
        db.session.commit()
        # return the updated card back
        return genre_schema.dump(genre)
    # else
    else:
        # return error msg
        return {"error": f"Genre with id {genre_id} not found"}, 404


# http://localhost:8080/genres/4/1 - POST
@genres_bp.route("/<int:genre_id>/<int:game_id>", methods=["POST"])
@jwt_required()
def assign_game_genre(genre_id, game_id):
    # Check if user is an admin
    is_admin = is_user_admin()
    if not is_admin:
        return {
            "error": "User is not authorised to assign a genre to a game"
        }, 403
    # Create a new game_genre model instance
    game_genre = Game_genre(game_id=game_id, genre_id=genre_id)
    # Add that to the session and commit
    db.session.add(game_genre)
    db.session.commit()
    # return the newly assigned genre
    return game_genre_schema.dump(game_genre), 201


# http://localhost:8080/genres/6 - DELETE
@genres_bp.route("/<int:genre_id>/<int:game_id>", methods=["DELETE"])
@jwt_required()
def delete_game_genre(genre_id, game_id):
    # Check if user is an admin
    is_admin = is_user_admin()
    if not is_admin:
        return {
            "error": "User is not authorised to delete a genre from a game"
        }, 403
    # get the genre from the db with genre_id = genre_id
    stmt = db.select(Game_genre).where(
        Game_genre.genre_id == genre_id and Game_genre.game_id == game_id
    )
    game_genre = db.session.scalar(stmt)
    stmt = db.select(Game).where(Game.game_id == game_id)
    game = db.session.scalar(stmt)
    stmt = db.select(Genre).where(Genre.genre_id == genre_id)
    genre = db.session.scalar(stmt)
    # if game_genre exists
    if game_genre:
        # delete the game_genre from the session and commit
        db.session.delete(game_genre)
        db.session.commit()
        # return msg

        return {
            "message": f"Genre '{genre.genre_name}' has been successfully deleted from the game '{game.game_title}'"
        }
    # else
    else:
        # return error msg
        return {
            "error": f"Genre '{genre.genre_name}' is not assigned to the game '{game.game_title}'"
        }, 404
