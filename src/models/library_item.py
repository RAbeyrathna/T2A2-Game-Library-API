from init import db, ma
from marshmallow import fields
from sqlalchemy import UniqueConstraint


class Library_item(db.Model):
    __tablename__ = "library_items"

    library_item_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)
    score = db.Column(db.Integer)

    user_library_id = db.Column(
        db.Integer,
        db.ForeignKey("user_library.user_library_id"),
        nullable=False,
    )

    game_id = db.Column(
        db.Integer, db.ForeignKey("games.game_id"), nullable=False
    )

    user_library = db.relationship(
        "User_library", back_populates="library_items"
    )

    game = db.relationship("Game", back_populates="library_items")

    __table_args__ = (
        UniqueConstraint(
            "game_id", "user_library_id", name="unique_game_entry"
        ),
    )


class Library_Item_Schema(ma.Schema):

    user_library = fields.Nested(
        "User_Library_Schema", exclude=["library_items"]
    )
    game = fields.Nested("GameSchema", only=["game_id", "game_title"])

    class Meta:
        fields = ("user_library", "library_item_id", "game", "status", "score")
        ordered = True


library_item_schema = Library_Item_Schema()
library_items_schema = Library_Item_Schema(many=True)