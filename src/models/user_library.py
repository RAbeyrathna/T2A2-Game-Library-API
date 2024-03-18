from init import db, ma
from marshmallow import fields


class User_library(db.Model):
    __tablename__ = "user_library"

    user_library_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.user_id"), nullable=False
    )

    user = db.relationship("User", back_populates="user_library")

    library_items = db.relationship(
        "Library_item", back_populates="user_library", cascade="all, delete"
    )


class User_Library_Schema(ma.Schema):

    user = fields.Nested("UserSchema", only=["username"])

    library_items = fields.List(
        fields.Nested("Library_Item_Schema", exclude=["user_library"])
    )

    class Meta:
        fields = ("user_library_id", "user", "library_items")
        ordered = True


user_library_schema = User_Library_Schema()
user_libraries_schema = User_Library_Schema(many=True)
