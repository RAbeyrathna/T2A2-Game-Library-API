from init import db, ma
from marshmallow import fields


class Platform(db.Model):
    __tablename__ = "platforms"

    platform_id = db.Column(db.Integer, primary_key=True)
    platform_name = db.Column(db.String, nullable=False, unique=True)
    platform_type = db.Column(db.String, nullable=False)

    game_platforms = db.relationship(
        "Game_platform", back_populates="platform", cascade="all, delete"
    )


class PlatformSchema(ma.Schema):

    game_platforms = fields.List(
        fields.Nested("Game_Platform_Schema", exclude=["platform"])
    )

    class Meta:
        fields = (
            "platform_id",
            "platform_name",
            "platform_type",
            "game_platforms",
        )


platform_schema = PlatformSchema()
platforms_schema = PlatformSchema(many=True)
