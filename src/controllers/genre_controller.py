from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from init import db
from models.genre import Genre, genre_schema, genres_schema
from models.game_genre import Game_genre, game_genre_schema
from models.game import Game

from controllers.auth_controller import authorise_as_admin

genres_bp = Blueprint("genres", __name__, url_prefix="/genres")


# Route to get all genres from the database
# # http://localhost:8080/genres - GET
@genres_bp.route("/")
def get_all_genres():

    # SELECT * FROM genres;
    stmt = db.select(Genre)
    genres = db.session.scalars(stmt)

    # Return all genre records in database
    return genres_schema.dump(genres)


# Route to get an individual genre from the database
# # http://localhost:8080/genres/1 - GET
# Assume genre_id = 1
@genres_bp.route("/<int:genre_id>")
def get_one_genre(genre_id):

    # SELECT * FROM genres WHERE genre_id = 1;
    stmt = db.select(Genre).filter_by(genre_id=genre_id)
    genre = db.session.scalar(stmt)

    # If genre record exists, return to user
    if genre:
        return genre_schema.dump(genre)
    # Else, return error that genre record not found
    else:
        return {"error": f"Genre with id {genre_id} not found"}, 404


# Route to get create a genre in the database
# http://localhost:8080/genres - POST
@genres_bp.route("/", methods=["POST"])
@jwt_required()
# User must be an admin to use this function
@authorise_as_admin  # # is_admin = True
def create_genre():
    # Get the genre data from the body of the request
    body_data = genre_schema.load(request.get_json())

    # Create a new genre model instance
    genre = Genre(genre_name=body_data.get("genre_name"))

    # Add that to the session and commit
    db.session.add(genre)
    db.session.commit()

    # return the newly created genre
    return genre_schema.dump(genre), 201


# Route to get delete a genre from the database
# http://localhost:8080/genres/2 - DELETE
# Assume genre_id = 2
@genres_bp.route("/<int:genre_id>", methods=["DELETE"])
@jwt_required()
@authorise_as_admin  # is_admin = True
def delete_genre(genre_id):

    # SELECT * FROM genres WHERE genre_id = 2;
    stmt = db.select(Genre).where(Genre.genre_id == genre_id)
    genre = db.session.scalar(stmt)

    # If genre record exists
    if genre:
        # Delete the genre from the session and commit
        db.session.delete(genre)
        db.session.commit()
        # Return message to confirm deletion completed
        return {
            "message": f"Genre '{genre.genre_name}' has been deleted successfully"
        }
    # Else, return error message
    else:
        return {"error": f"Genre with id {genre_id} not found"}, 404


# Route to get update a genre from the database
# http://localhost:8080/genres/5 - PUT, PATCH
# Assume genre_id = 5
@genres_bp.route("/<int:genre_id>", methods=["PUT", "PATCH"])
@jwt_required()
@authorise_as_admin  # is_admin = True
def update_genre(genre_id):

    # Get the genre data to be updated from the body of the request
    body_data = genre_schema.load(request.get_json(), partial=True)

    # SELECT * FROM genres where genre_id = 5;
    stmt = db.select(Genre).filter_by(genre_id=genre_id)
    genre = db.session.scalar(stmt)

    # If genre record exists, update the fields given
    if genre:
        genre.genre_name = body_data.get("genre_name") or genre.genre_name
        db.session.commit()
        # Return the updated genre back
        return genre_schema.dump(genre)

    # Else return an error message
    else:
        return {"error": f"Genre with id {genre_id} not found"}, 404


# Route to assign a genre to a game
# http://localhost:8080/genres/4/game/1 - POST
# Assume genre_id = 4 and game_id = 1
@genres_bp.route("/<int:genre_id>/game/<int:game_id>", methods=["POST"])
@jwt_required()
@authorise_as_admin  # is_admin = True
def assign_game_genre(genre_id, game_id):

    # Create a new game_genre model instance
    game_genre = Game_genre(game_id=game_id, genre_id=genre_id)

    # Add that to the session and commit
    db.session.add(game_genre)
    db.session.commit()

    # Return the newly assigned genre and game
    return game_genre_schema.dump(game_genre), 201


# Route to delete a genre from a game
# http://localhost:8080/genres/4/game/1 - DELETE
# Assume genre_id = 4 and game_id = 1
@genres_bp.route("/<int:genre_id>/game/<int:game_id>", methods=["DELETE"])
@jwt_required()
@authorise_as_admin  # is_admin = True
def delete_game_genre(genre_id, game_id):

    # SELECT * FROM game_genres WHERE genre_id = 4 AND game_id = 1;
    stmt = db.select(Game_genre).where(
        Game_genre.genre_id == genre_id and Game_genre.game_id == game_id
    )
    game_genre = db.session.scalar(stmt)

    # Get game record with same game_id to use in return message
    # SELECT * FROM games WHERE game_id = 1;
    stmt = db.select(Game).where(Game.game_id == game_id)
    game = db.session.scalar(stmt)

    # Get genre record with same genre_id to use in return message
    # SELECT * FROM genres WHERE genre_id = 4;
    stmt = db.select(Genre).where(Genre.genre_id == genre_id)
    genre = db.session.scalar(stmt)

    # If game_genre record exists. delete the record from the session and commit
    if game_genre:
        db.session.delete(game_genre)
        db.session.commit()
        return {
            "message": f"Genre '{genre.genre_name}' has been successfully deleted from the game '{game.game_title}'"
        }, 201
    # Else, return error that the genre is not assigned to specified game
    else:
        return {
            "error": f"Genre '{genre.genre_name}' is not assigned to the game '{game.game_title}'"
        }, 404
