from init import db, ma


class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    publisher = db.Column(db.String)
    description = db.Column(db.String)
    release_date = db.Column(db.Date)
    metacritic_score = db.Column(db.Integer)


class GameSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "title",
            "publisher",
            "description",
            "release_date",
            "metacritic_score",
        )


game_schema = GameSchema()
game_schemas = GameSchema(many=True)
