from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from init import db
from models.game import Game, game_schema, games_schema

from controllers.auth_controller import is_user_admin

games_bp = Blueprint("games", __name__, url_prefix="/games")


# # http://localhost:8080/games - GET
@games_bp.route("/")
def get_all_games():
    stmt = db.select(Game)
    games = db.session.scalars(stmt)
    return games_schema.dump(games)


# # http://localhost:8080/games/1 - GET
@games_bp.route("/<int:game_id>")
def get_one_game(game_id):  # game_id = 1
    stmt = db.select(Game).filter_by(
        game_id=game_id
    )  # select * from games where game_id = 1
    game = db.session.scalar(stmt)
    if game:
        return game_schema.dump(game)
    else:
        return {"error": f"Game with id {game_id} not found"}, 404


# http://localhost:8080/games - POST
@games_bp.route("/", methods=["POST"])
@jwt_required()
def create_game():
    # Check if user is an admin
    is_admin = is_user_admin()
    if not is_admin:
        return {"error": "User is not authorised to create a game"}, 403
    body_data = game_schema.load(request.get_json())
    # Create a new game model instance
    game = Game(
        game_title=body_data.get("game_title"),
        description=body_data.get("description"),
        publisher=body_data.get("publisher"),
        release_date=body_data.get("release_date"),
        metacritic_score=body_data.get("metacritic_score"),
    )
    # Add that to the session and commit
    db.session.add(game)
    db.session.commit()
    # return the newly created game
    return game_schema.dump(game), 201


# http://localhost:8080/games/6 - DELETE
@games_bp.route("/<int:game_id>", methods=["DELETE"])
@jwt_required()
def delete_game(game_id):
    # Check if user is an admin
    is_admin = is_user_admin()
    if not is_admin:
        return {"error": "User is not authorised to delete a game"}, 403
    # get the game from the db with game_id = game_id
    stmt = db.select(Game).where(Game.game_id == game_id)
    game = db.session.scalar(stmt)
    # if game exists
    if game:
        # delete the game from the session and commit
        db.session.delete(game)
        db.session.commit()
        # return msg
        return {
            "message": f"Game '{game.game_title}' has been deleted successfully"
        }
    # else
    else:
        # return error msg
        return {"error": f"Game with id {game_id} not found"}, 404


# http://localhost:8080/games/5 - PUT, PATCH
@games_bp.route("/<int:game_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_game(game_id):
    # Check if user is an admin
    is_admin = is_user_admin()
    if not is_admin:
        return {"error": "User is not authorised to edit a game"}, 403
    # Get the data to be updated from the body of the request
    body_data = game_schema.load(request.get_json(), partial=True)
    # get the game from the db whose fields need to be updated
    stmt = db.select(Game).filter_by(game_id=game_id)
    game = db.session.scalar(stmt)
    # if game exists
    if game:
        # update the fields
        game.game_title = body_data.get("game_title") or game.game_title
        game.description = body_data.get("description") or game.description
        game.publisher = body_data.get("publisher") or game.publisher
        game.release_date = body_data.get("release_date") or game.release_date
        game.metacritic_score = (
            body_data.get("metacritic_score") or game.metacritic_score
        )
        # commit the changes
        db.session.commit()
        # return the updated game back
        return game_schema.dump(game)
    # else
    else:
        # return error msg
        return {"error": f"Game with id {game_id} not found"}, 404
