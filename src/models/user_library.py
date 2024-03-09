from init import db, ma
from marshmallow import fields


class User_library(db.Model):
    __tablename__ = "user_library"

    user_library_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="user_library")


class User_LibrarySchema(ma.Schema):

    user = fields.Nested("UserSchema", only=["username", "email"])

    comments = fields.List(fields.Nested("CommentSchema", exclude=["card"]))

    class Meta:
        fields = (
            "id",
            "user",
        )
        ordered = True


user_library_schema = User_LibrarySchema()
# user_libraries_schema = User_LibrarySchema(many=True)
