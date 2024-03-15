from datetime import timedelta
import functools

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity

from init import db, bcrypt
from models.user import User, user_schema
from models.user_library import User_library

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# Route to create user account on web server
# # http://localhost:8080/auth/register - POST
@auth_bp.route("/register", methods=["POST"])
def auth_register():

    # Get the user data from the body of the request
    body_data = user_schema.load(request.get_json())

    # Create user instance
    user = User(
        username=body_data.get("username"),
        email=body_data.get("email"),
    )
    # Get password from the request body
    password = body_data.get("password")
    # Check if password exists, if it does, hash it
    if password:
        user.password = bcrypt.generate_password_hash(password).decode("utf-8")

    # Create user and user library, then commit to session
    db.session.add(user)

    user_library = User_library(user=user)
    db.session.add(user_library)
    db.session.commit()

    # Respond back to client with user details and library_id
    return user_schema.dump(user), 201


# Route to login using registered user account in database
# # http://localhost:8080/auth/login - POST
@auth_bp.route("/login", methods=["POST"])
def auth_login():

    # Get the data from the request body
    body_data = user_schema.load(request.get_json())

    # Find user with the email address
    # SELECT * FROM users WHERE email = 'user_email_here';
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)

    # If cannot find user account with email, return account not found error
    if not user:
        return {"error": "Invalid email. User does not exist"}, 401

    # if given password does not match hashed password in database, return password error
    if not bcrypt.check_password_hash(
        user.password, body_data.get("password")
    ):
        return {"error": "Password is incorrect"}, 401

    # Assuming account was found, create JWT
    token = create_access_token(
        identity=str(user.user_id), expires_delta=timedelta(days=1)
    )
    # Return the token along with the user info
    return {"email": user.email, "token": token, "is_admin": user.is_admin}


# Function to check if user account is an admin (checking the is_admin field)
def is_user_admin():

    # Get user_id from the JWT token
    user_id = int(get_jwt_identity())

    # Find the user record with the user_id
    # SELECT * FROM users where user_id = jwt_user_id
    stmt = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(stmt)

    # For edge case where old JWT token is used for a deleted account
    if user is None:
        return {
            "error": "The logged in user has been deleted. Please login again."
        }, 403

    # Return True if user is admin, otherwise False
    return user.is_admin


# Decorator function to make sure user account is an admin (for games, platforms and genre routes)
def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):

        # Get user_id from the JWT token
        user_id = int(get_jwt_identity())

        # SELECT * FROM users where user_id = jwt_user_id
        stmt = db.select(User).filter_by(user_id=user_id)
        user = db.session.scalar(stmt)

        # For edge case where old JWT token is used for a deleted account
        if user is None:
            return {
                "error": "The logged in user has been deleted. Please login again."
            }, 403

        # Run the decorated function if user is admin
        if user.is_admin:
            return fn(*args, **kwargs)

        # Else, return error that user is not an admin
        else:
            return {
                "error": "User account does not have admin privilleges"
            }, 403

    return wrapper
