import functools

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_jwt_extended import jwt_required

from init import db, bcrypt
from models.user import User, user_schema, users_schema
from models.user_library import User_library

from controllers.auth_controller import is_user_admin

user_bp = Blueprint("users", __name__, url_prefix="/users")


def account_owner(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = int(get_jwt_identity())
        user_id = kwargs.get("user_id")
        stmt = db.select(User).filter_by(user_id=user_id)
        user = db.session.scalar(stmt)

        is_admin = is_user_admin()
        if user and (user.user_id == current_user_id or is_admin):
            return fn(*args, **kwargs)
        else:
            return {"error": "User is not the owner of this account"}, 403

    return wrapper


# # http://localhost:8080/users/1 - GET
@jwt_required
@user_bp.route("/")
def get_all_users():
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return users_schema.dump(users)


# # http://localhost:8080/users/ - GET
@user_bp.route("/<int:user_id>")
def get_one_user(user_id):  # user_id = 1
    stmt = db.select(User).filter_by(
        user_id=user_id
    )  # select * from user where user_id = 1
    user = db.session.scalar(stmt)
    if user:
        return user_schema.dump(user)
    else:
        return {"error": f"User with id {user_id} not found"}, 404


# http://localhost:8080/users/6 - DELETE
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@account_owner
def delete_user(user_id):
    stmt = db.select(User).where(User.user_id == user_id)
    user = db.session.scalar(stmt)
    # if user exists
    if user:
        # delete the user from the session and commit
        db.session.delete(user)
        db.session.commit()
        # return msg
        return {
            "message": f"User with ID '{user.user_id}' has been deleted successfully"
        }, 200
    # else
    else:
        # return error msg
        return {"error": f"User with ID {user_id} was not found"}, 404


# http://localhost:8080/users/5 - PUT, PATCH
@user_bp.route("/<int:user_id>", methods=["PUT", "PATCH"])
@jwt_required()
@account_owner
def update_user(user_id):
    # Get the data to be updated from the body of the request
    body_data = user_schema.load(request.get_json(), partial=True)
    # get the game from the db whose fields need to be updated
    stmt = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(stmt)
    # if user exists
    if user:
        # update the fields
        user.username = body_data.get("username") or user.username
        user.email = body_data.get("email") or user.email

        password = body_data.get("password")
        # Check if password exists, if it does, hash it
        if password:
            user.password = bcrypt.generate_password_hash(password).decode(
                "utf-8"
            )
        else:
            user.password
        # commit the changes
        db.session.commit()
        # return the updated game back
        return user_schema.dump(user)
    # else
    else:
        # return error msg
        return {"error": f"User with ID {user_id} not found"}, 404
