from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, OneOf, And

VALID_PLATFORM_TYPES = (
    "PC",
    "Console",
    "Handheld",
    "Hybrid",
    "Home Console",
    "Cloud Gaming",
)


class Platform(db.Model):
    __tablename__ = "platforms"

    platform_id = db.Column(db.Integer, primary_key=True)
    platform_name = db.Column(db.String, nullable=False, unique=True)
    platform_type = db.Column(db.String, nullable=False)

    game_platforms = db.relationship(
        "Game_platform", back_populates="platform", cascade="all, delete"
    )


class PlatformSchema(ma.Schema):
    platform_id = fields.Integer()
    platform_name = fields.String(
        required=True,
        validate=Length(
            min=2,
            error="Platform name must have a length of at least 2 characters",
        ),
    )

    platform_type = fields.String(
        required=True, validate=OneOf(VALID_PLATFORM_TYPES)
    )

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
