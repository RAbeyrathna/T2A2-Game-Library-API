from init import db, ma
from marshmallow import fields
from sqlalchemy import UniqueConstraint


class Game_platform(db.Model):
    __tablename__ = "game_platforms"

    game_platforms_id = db.Column(db.Integer, primary_key=True)

    game_id = db.Column(
        db.Integer, db.ForeignKey("games.game_id"), nullable=False
    )

    platform_id = db.Column(
        db.Integer, db.ForeignKey("platforms.platform_id"), nullable=False
    )

    game = db.relationship("Game", back_populates="game_platforms")
    platform = db.relationship("Platform", back_populates="game_platforms")

    __table_args__ = (
        UniqueConstraint(
            "game_id", "platform_id", name="unique_game_platform"
        ),
    )


class Game_Platform_Schema(ma.Schema):

    game = fields.Nested("GameSchema", only=["game_id", "game_title"])
    platform = fields.Nested("PlatformSchema")

    class Meta:
        fields = ("game_platforms_id", "game", "platform")
        ordered = True


game_genre_schema = Game_Platform_Schema()
game_genres_schema = Game_Platform_Schema(many=True)
