from init import db, ma


class Genre(db.Model):
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String, nullable=False)


class GenreSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "genre_name",
        )


genre_schema = GenreSchema()
genre_schemas = GenreSchema(many=True)
