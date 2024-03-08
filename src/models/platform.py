from init import db, ma


class Platform(db.Model):
    __tablename__ = "platforms"

    id = db.Column(db.Integer, primary_key=True)
    platform_name = db.Column(db.String, nullable=False)
    platform_type = db.Column(db.String, nullable=False)


class PlatformSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "platform_name",
            "platform_type",
        )


platform_schema = PlatformSchema()
platform_schemas = PlatformSchema(many=True)
