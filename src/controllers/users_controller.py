import functools

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from init import db, bcrypt
from models.user import User, user_schema, users_schema

from controllers.auth_controller import is_user_admin

user_bp = Blueprint("users", __name__, url_prefix="/users")


# Decorator function to check if logged in user owns the account being accessed
def account_owner(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):

        # Get logged in user_id from JWT
        current_user_id = int(get_jwt_identity())

        # Get 'accessed' user_id from route
        user_id = kwargs.get("user_id")

        # Get user record from database using 'route user_id'
        # SELECT * FROM USER where user_id = user_id
        stmt = db.select(User).filter_by(user_id=user_id)
        user = db.session.scalar(stmt)

        # Checks if user has admin permissions
        is_admin = is_user_admin()

        # If user is an admin OR logged in user_id is the same as recorc user_id
        # # Continue running the decorated function
        if user and (user.user_id == current_user_id or is_admin):
            return fn(*args, **kwargs)

        # If user account is not found with specified ID, return error
        elif not user:
            return {
                "error": f"User account with ID '{user_id}' does not exist"
            }, 403

        # Else, return error that user is not the owner of the account
        else:
            return {"error": "User is not the owner of this account"}, 403

    return wrapper


# Route to get ALL users from the database
# # http://localhost:8080/users/ - GET
@jwt_required
@user_bp.route("/")
def get_all_users():

    # SELECT * FROM users;
    stmt = db.select(User)
    users = db.session.scalars(stmt)

    # Return response with all currently registered users
    return users_schema.dump(users)


# Route to get an individual user from the database
# # http://localhost:8080/users/1 - GET
# # Assume user_id = 1
@user_bp.route("/<int:user_id>")
def get_one_user(user_id):

    # Get user record from database using provided user_id
    # SELECT * FROM users WHERE user_id = 1;
    stmt = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(stmt)

    # If user record exists, return the record
    if user:
        return user_schema.dump(user)

    # Else, return error that user_id does not exist in database
    else:
        return {"error": f"User with id {user_id} not found"}, 404


# Route to delete a specific user from the database
# # http://localhost:8080/users/6 - DELETE
# # Assume user_id = 6
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@account_owner  # Make sure user owns the account or is an admin
def delete_user(user_id):

    # Get user record from database using provided user_id
    # SELECT * FROM users where User.user_id == 6
    stmt = db.select(User).where(User.user_id == user_id)
    user = db.session.scalar(stmt)

    # If user record exists
    if user:

        # Delete the user from the session and commit
        db.session.delete(user)
        db.session.commit()

        # Return msg that deletion has been completed
        return {
            "message": f"User with ID '{user_id}' has been deleted successfully"
        }, 200

    # Return error message that user_id was not found
    else:
        return {"error": f"User with ID {user_id} was not found"}, 404


# Route to update a specific user from the database
# http://localhost:8080/users/5 - PUT, PATCH
# # Assume user_id = 5
@user_bp.route("/<int:user_id>", methods=["PUT", "PATCH"])
@jwt_required()
@account_owner
def update_user(user_id):

    # Get the data to be updated from the body of the request
    body_data = user_schema.load(request.get_json(), partial=True)

    # Get the user record from the DB
    stmt = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(stmt)

    # If user record exists, update the fields
    if user:
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

        # Commit the changes
        db.session.commit()

        # Return the updated user back
        return user_schema.dump(user)
    # Else, return error message that user_id was not found
    else:

        return {"error": f"User with ID {user_id} not found"}, 404
