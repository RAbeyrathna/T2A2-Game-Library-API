from init import db, ma
from marshmallow import fields


class Game(db.Model):
    __tablename__ = "games"

    game_id = db.Column(db.Integer, primary_key=True)
    game_title = db.Column(db.String, nullable=False)
    publisher = db.Column(db.String)
    description = db.Column(db.String)
    release_date = db.Column(db.Date)
    metacritic_score = db.Column(db.Integer)

    game_genres = db.relationship(
        "Game_genre", back_populates="game", cascade="all, delete"
    )

    game_platforms = db.relationship(
        "Game_platform", back_populates="game", cascade="all, delete"
    )

    library_items = db.relationship(
        "Library_item", back_populates="game", cascade="all, delete"
    )


class GameSchema(ma.Schema):

    game_genres = fields.List(
        fields.Nested("Game_Genre_Schema", exclude=["game"])
    )

    game_platforms = fields.List(
        fields.Nested("Game_Platform_Schema", exclude=["game"])
    )

    class Meta:
        fields = (
            "game_id",
            "game_title",
            "publisher",
            "description",
            "release_date",
            "metacritic_score",
            "game_genres",
            "game_platforms",
        )


game_schema = GameSchema()
games_schema = GameSchema(many=True)
