from datetime import date

from flask import Blueprint

from init import db, bcrypt
from models.user import User

db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables have been created")


@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("All tables have been dropped")


@db_commands.cli.command("seed")
def seed_tables():
    users = [
        User(
            username="Admin Account",
            email="admin@email.com",
            password=bcrypt.generate_password_hash("123456").decode("utf-8"),
            is_admin=True,
        ),
        User(
            username="Test User 1",
            email="user1@email.com",
            password=bcrypt.generate_password_hash("123456").decode("utf-8"),
        ),
    ]

    db.session.add_all(users)

    db.session.commit()

    print("Tables have been seeded")


@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("All tables have been dropped")
