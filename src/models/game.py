from datetime import datetime

from init import db, ma
from marshmallow import fields, validates, ValidationError

from marshmallow.validate import Length, And, Regexp, Range


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

    game_id = fields.Integer()
    game_title = fields.String(
        required=True,
        validate=And(
            Length(
                min=2,
                error="Game title must have a length of at least 2 characters",
            ),
            Regexp(
                "^[a-zA-Z0-9\s\-_&.'()! ]+$",
                error="Game title cannot contain special characters such as @, #, $, %, *, /, question marks, colons, semicolons, and brackets",
            ),
        ),
    )
    publisher = fields.String(
        required=True,
        validate=And(
            Length(
                min=2,
                error="Publisher must have a length of at least 2 characters",
            ),
            Regexp(
                "^[a-zA-Z0-9\s\-_&.,'()! ]+$",
                error="Publisher cannot contain special characters such as @, #, $, %, *, /, question marks, colons, semicolons, and brackets",
            ),
        ),
    )
    release_date = fields.Date(
        format="%Y-%m-%d",
        error_messages={"error": "Invalid date format. Use YYYY-MM-DD."},
    )

    @validates("release_date")
    def validate_release_date(self, value):
        if value > datetime.now().date():
            raise ValidationError("Release date cannot be in the future.")

    metacritic_score = fields.Integer(
        validate=Range(
            min=0,
            max=100,
            error="Score must be between 0 - 100",
        ),
    )

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
