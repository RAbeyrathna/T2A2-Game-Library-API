from init import db, ma

from marshmallow import fields

from sqlalchemy import UniqueConstraint


class Game_genre(db.Model):
    __tablename__ = "game_genres"

    game_genres_id = db.Column(db.Integer, primary_key=True)

    game_id = db.Column(
        db.Integer, db.ForeignKey("games.game_id"), nullable=False
    )

    genre_id = db.Column(
        db.Integer, db.ForeignKey("genres.genre_id"), nullable=False
    )

    game = db.relationship("Game", back_populates="game_genres")
    genre = db.relationship("Genre", back_populates="game_genres")

    __table_args__ = (
        UniqueConstraint("game_id", "genre_id", name="unique_game_genre"),
    )


class Game_Genre_Schema(ma.Schema):

    game = fields.Nested("GameSchema", only=["game_id", "game_title"])

    genre = fields.Nested("GenreSchema", only=["genre_id", "genre_name"])

    class Meta:
        fields = ("game_genres_id", "genre", "game")
        ordered = True


game_genre_schema = Game_Genre_Schema()
game_genres_schema = Game_Genre_Schema(many=True)
