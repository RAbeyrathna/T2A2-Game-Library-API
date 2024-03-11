from init import db, ma
from marshmallow import fields


class Genre(db.Model):
    __tablename__ = "genres"

    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String, nullable=False)

    game_genres = db.relationship(
        "Game_genre", back_populates="genre", cascade="all, delete"
    )


class GenreSchema(ma.Schema):

    game_genres = fields.List(
        fields.Nested("Game_Genre_Schema", exclude=["genre"])
    )

    class Meta:
        fields = ("genre_id", "genre_name", "game_genres")


genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)
