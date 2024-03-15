from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from init import db
from models.game import Game, game_schema, games_schema

from controllers.auth_controller import authorise_as_admin

games_bp = Blueprint("games", __name__, url_prefix="/games")


# Route to get all games from the database
# # http://localhost:8080/games - GET
@games_bp.route("/")
def get_all_games():

    # SELECT * FROM games;
    stmt = db.select(Game)
    games = db.session.scalars(stmt)

    # Return all game records in database
    return games_schema.dump(games)


# Route to get an individual game record from the database
# # http://localhost:8080/games/1 - GET
# Assume game_id = 1
@games_bp.route("/<int:game_id>")
def get_one_game(game_id):

    # SELECT * FROM games WHERE game_id = 1;
    stmt = db.select(Game).filter_by(game_id=game_id)
    game = db.session.scalar(stmt)

    # If game record exists in DB, return to user
    if game:
        return game_schema.dump(game)
    # Else return error message that game record with ID not found
    else:
        return {"error": f"Game with id {game_id} not found"}, 404


# Route to get create a game in the database
# http://localhost:8080/games - POST
@games_bp.route("/", methods=["POST"])
@jwt_required()
# User must be an admin to use this function
@authorise_as_admin  # is_admin = True
def create_game():

    # Get the game data from the body of the request
    body_data = game_schema.load(request.get_json())

    # Create a new game model instance
    game = Game(
        game_title=body_data.get("game_title"),
        description=body_data.get("description"),
        publisher=body_data.get("publisher"),
        release_date=body_data.get("release_date"),
        metacritic_score=body_data.get("metacritic_score"),
    )

    # Add game data to the session and commit
    db.session.add(game)
    db.session.commit()

    # Return the newly created game
    return game_schema.dump(game), 201


# Route to get delete a game from the database
# http://localhost:8080/games/6 - DELETE
# Assume game_id = 6
@games_bp.route("/<int:game_id>", methods=["DELETE"])
@jwt_required()
@authorise_as_admin  # is_admin = True
def delete_game(game_id):

    # SELECT * FROM games WHERE game_id = 6;
    stmt = db.select(Game).where(Game.game_id == game_id)
    game = db.session.scalar(stmt)

    # If Game record exists, delete the game from the session and commit
    if game:
        db.session.delete(game)
        db.session.commit()
        return {
            "message": f"Game '{game.game_title}' has been deleted successfully"
        }

    # Else return an error message
    else:
        return {"error": f"Game with id {game_id} not found"}, 404


# Route to get update a game from the database
# http://localhost:8080/games/6 - PUT, PATCH
# Assume game_id = 6
@games_bp.route("/<int:game_id>", methods=["PUT", "PATCH"])
@jwt_required()
@authorise_as_admin  # is_admin = True
def update_game(game_id):

    # Get the game data to be updated from the body of the request
    body_data = game_schema.load(request.get_json(), partial=True)

    # SELECT * FROM games WHERE game_id = 6;
    stmt = db.select(Game).filter_by(game_id=game_id)
    game = db.session.scalar(stmt)

    # If Game record exists, update the specified fields
    if game:
        game.game_title = body_data.get("game_title") or game.game_title
        game.description = body_data.get("description") or game.description
        game.publisher = body_data.get("publisher") or game.publisher
        game.release_date = body_data.get("release_date") or game.release_date
        game.metacritic_score = (
            body_data.get("metacritic_score") or game.metacritic_score
        )

        # Commit the changes
        db.session.commit()

        # Return the updated game back
        return game_schema.dump(game)

    # Else return an error message
    else:
        return {"error": f"Game with id {game_id} not found"}, 404
