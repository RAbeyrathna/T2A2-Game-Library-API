from init import db, ma
from marshmallow import fields


class Game(db.Model):
    __tablename__ = "games"

    game_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    publisher = db.Column(db.String)
    description = db.Column(db.String)
    release_date = db.Column(db.Date)
    metacritic_score = db.Column(db.Integer)

    game_genres = db.relationship(
        "Game_genre", back_populates="game", cascade="all, delete"
    )  # Add nullable = False once all other fields set so can assign a game genre


class GameSchema(ma.Schema):

    game_genres = fields.List(
        fields.Nested("Game_Genre_Schema", exclude=["game"])
    )

    class Meta:
        fields = (
            "game_id",
            "title",
            "publisher",
            "description",
            "release_date",
            "metacritic_score",
            "game_genres",
        )


game_schema = GameSchema()
game_schemas = GameSchema(many=True)
