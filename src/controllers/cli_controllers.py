from datetime import date

from flask import Blueprint

from init import db, bcrypt
from models.user import User
from models.game import Game

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
    games = [
        Game(
            title="Pokemon Emerald",
            publisher="Nintendo",
            description="Pokémon Emerald Version takes Trainers back to the land of Hoenn for an expanded adventure, this time against both Team Magma and Team Aqua! Pokémon Emerald also features an even more exciting storyline featuring the Legendary Rayquaza, and the chance to catch more Legendary Pokémon such as both Latios and Latias!",
            release_date=date(2004, 9, 9),
            metacritic_score=76,
        ),
        Game(
            title="Balatro",
            publisher="Playstack",
            description="Balatro is a hypnotically satisfying deckbuilder where you play illegal poker hands, discover game-changing jokers, and trigger adrenaline-pumping, outrageous combos. Combine valid poker hands with unique Joker cards in order to create varied synergies and builds",
            release_date=date(2024, 2, 20),
            metacritic_score=90,
        ),
        Game(
            title="Slay The Spire",
            publisher="Mega Crit Games",
            description="You are an adventurer ascending a spire in order to slay it. Your cards attack and defend and do all sorts of things. Beating enemies allows you to put more cards in your deck and earn gold that can be spent on shops. Each act has sixteen floors, the last of which is a boss fight; beat three acts to win a run",
            release_date=date(2019, 5, 21),
            metacritic_score=89,
        ),
        Game(
            title="God of War",
            publisher="Sony Interactive Entertainment",
            description="His vengeance against the Gods of Olympus behind him, Kratos now lives in the realm of Norse deities and monsters. It's in this harsh, unforgiving world that he must fight to survive, and not only teach his son to do the same… but also prevent him from repeating the Ghost of Sparta's bloodstained mistakes",
            release_date=date(2018, 4, 20),
            metacritic_score=94,
        ),
        Game(
            title="Psychonauts",
            publisher="Double Fine Productions",
            description="Psychonauts is a platform game that incorporates various adventure elements. The player controls the main character Raz in a third-person, three-dimensional view, helping Raz to uncover a mystery at the Psychonauts training camp.",
            release_date=date(2005, 4, 19),
            metacritic_score=88,
        ),
        Game(
            title="Pyre",
            publisher="Supergiant Games",
            description="A party-based RPG from the creators of Bastion and Transistor. Lead your band of exiles to freedom through a series of mystical competitions in the Campaign, or challenge a friend to a fast-paced ritual showdown in the head-to-head Versus Mode.",
            release_date=date(2017, 7, 25),
            metacritic_score=85,
        ),
    ]
    db.session.add_all(games)
    db.session.commit()

    print("Tables have been seeded")


@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("All tables have been dropped")
