from init import db, ma
from marshmallow import fields


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

    user_library = fields.Nested("User_Library_Schema", exclude=["user"])

    class Meta:
        fields = (
            "id",
            "username",
            "email",
            "password",
            "is_admin",
            "user_library",
        )


user_schema = UserSchema(exclude=["password"])
user_schemas = UserSchema(many=True, exclude=["password"])
