from datetime import timedelta
import functools

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_jwt_extended import jwt_required

from init import db, bcrypt
from models.user import User, user_schema
from models.user_library import User_library

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def auth_register():
    # Get the data from the body of the request
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

    # Respond back to client
    return user_schema.dump(user), 201


@auth_bp.route("/login", methods=["POST"])
def auth_login():
    # Get the data from the request body
    body_data = request.get_json()
    # Find user with the email address
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)
    # If user exists and password is correct
    if user and bcrypt.check_password_hash(
        user.password, body_data.get("password")
    ):
        # Create JWT
        token = create_access_token(
            identity=str(user.user_id), expires_delta=timedelta(days=1)
        )
        # Return the token along with the user info
        return {"email": user.email, "token": token, "is_admin": user.is_admin}
    # Else
    else:
        # Return error
        return {"error": "Invalid email or password"}, 401


def is_user_admin():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin


def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(user_id=user_id)
        user = db.session.scalar(stmt)
        if user.is_admin:
            # Run the decorated function if user is admin
            return fn(*args, **kwargs)
        else:
            return {
                "error": "User account does not have admin privilleges"
            }, 403

    return wrapper
