from init import db, ma
from marshmallow import fields

from marshmallow.validate import Length, And, Regexp


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    user_library = db.relationship(
        "User_library", back_populates="user", cascade="all, delete"
    )


class UserSchema(ma.Schema):

    username = fields.String(
        validate=And(
            Length(
                min=2,
                error="Username must have a length of at least 2 characters",
            ),
            Regexp(
                "^[a-zA-Z0-9\s\-_.'()! ]+$",
                error="Username cannot contain special characters such as @, &, #, $, %, *, /, question marks, colons, semicolons, and brackets",
            ),
        ),
    )
    email = fields.Email(required=True)
    password = fields.String(
        required=True,
        validate=And(
            Length(
                min=6, error="Password must be at least 6 characters long."
            ),
            Regexp(
                "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}$",
                error="Password must include at least one letter, one number, and one special character.",
            ),
        ),
        load_only=True,
    )

    user_library = fields.List(
        fields.Nested("User_Library_Schema", only=["user_library_id"])
    )

    class Meta:
        fields = (
            "user_id",
            "username",
            "email",
            "password",
            "is_admin",
            "user_library",
        )


user_schema = UserSchema()
users_schema = UserSchema(many=True)
