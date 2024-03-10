from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.user_library import User_library, user_library_schema


libraries_bp = Blueprint("cards", __name__, url_prefix="/library")


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


# # http://localhost:8080/cards - POST
# @cards_bp.route("/", methods=["POST"])
# @jwt_required()
# def create_card():
#     body_data = request.get_json()
#     # Create a new card model instance
#     card = Card(
#         title=body_data.get("title"),
#         description=body_data.get("description"),
#         date=date.today(),
#         status=body_data.get("status"),
#         priority=body_data.get("priority"),
#         user_id=get_jwt_identity(),
#     )
#     # Add that to the session and commit
#     db.session.add(card)
#     db.session.commit()
#     # return the newly created card
#     return card_schema.dump(card), 201


# # https://localhost:8080/cards/6 - DELETE
# @cards_bp.route("/<int:card_id>", methods=["DELETE"])
# def delete_card(card_id):
#     # get the card from the db with id = card_id
#     stmt = db.select(Card).where(Card.id == card_id)
#     card = db.session.scalar(stmt)
#     # if card exists
#     if card:
#         # delete the card from the session and commit
#         db.session.delete(card)
#         db.session.commit()
#         # return msg
#         return {"message": f"Card '{card.title}' deleted successfully"}
#     # else
#     else:
#         # return error msg
#         return {"error": f"Card with id {card_id} not found"}, 404


# # http://localhost:8080/cards/5 - PUT, PATCH
# @cards_bp.route("/<int:card_id>", methods=["PUT", "PATCH"])
# def update_card(card_id):
#     # Get the data to be updated from the body of the request
#     body_data = request.get_json()
#     # get the card from the db whose fields need to be updated
#     stmt = db.select(Card).filter_by(id=card_id)
#     card = db.session.scalar(stmt)
#     # if card exists
#     if card:
#         # update the fields
#         card.title = body_data.get("title") or card.title
#         card.description = body_data.get("description") or card.description
#         card.status = body_data.get("status") or card.status
#         card.priority = body_data.get("priority") or card.priority
#         # commit the changes
#         db.session.commit()
#         # return the updated card back
#         return card_schema.dump(card)
#     # else
#     else:
#         # return error msg
#         return {"error": f"Card with id {card_id} not found"}, 404


# # "/cards/<int:card_id>/comments" -> GET, POST
# # "/cards/5/comments" -> GET, POST

# # "/cards/<int:card_id>/comments/<int:comment_id>" -> PUT, PATCH, DELETE
# # "/cards/5/comments/2" -> PUT, PATCH, DELETE


# @cards_bp.route("/<int:card_id>/comments", methods=["POST"])
# @jwt_required()
# def create_comment(card_id):
#     body_data = request.get_json()
#     stmt = db.select(Card).filter_by(id=card_id)
#     card = db.session.scalar(stmt)
#     if card:
#         comment = Comment(
#             message=body_data.get("message"),
#             user_id=get_jwt_identity(),
#             card=card,
#         )
#         db.session.add(comment)
#         db.session.commit()
#         return comment_schema.dump(comment), 201
#     else:
#         return {"error": f"Card with id {card_id} doesn't exist"}, 404


# @cards_bp.route("/<int:card_id>/comments/<int:comment_id>", methods=["DELETE"])
# @jwt_required()
# def delete_comment(card_id, comment_id):
#     stmt = db.select(Comment).filter_by(id=comment_id)
#     comment = db.session.scalar(stmt)
#     if comment and comment.card.id == card_id:
#         db.session.delete(comment)
#         db.session.commit()
#         return {"message": f"Comment with id {comment_id} has been deleted"}
#     else:
#         return {
#             "error": f"Comment with id {comment_id} not found in card with id {card_id}"
#         }, 404


# @cards_bp.route(
#     "/<int:card_id>/comments/<int:comment_id>", methods=["PUT", "PATCH"]
# )
# @jwt_required()
# def edit_comment(card_id, comment_id):
#     body_data = request.get_json()
#     stmt = db.select(Comment).filter_by(id=comment_id, card_id=card_id)
#     comment = db.session.scalar(stmt)
#     if comment:
#         comment.message = body_data.get("message") or comment.message
#         db.session.commit()
#         return comment_schema.dump(comment)
#     else:
#         return {
#             "error": f"Comment with id {comment_id} not found in card with id {card_id}"
#         }
