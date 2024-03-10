from init import db, ma
from marshmallow import fields


class User_library(db.Model):
    __tablename__ = "user_library"

    user_library_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="user_library")


class User_Library_Schema(ma.Schema):

    user = fields.Nested("UserSchema", only=["username", "email"])

    class Meta:
        fields = (
            "id",
            "user",
        )
        ordered = True


user_library_schema = User_Library_Schema()
