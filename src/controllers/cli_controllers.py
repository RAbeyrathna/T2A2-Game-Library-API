from datetime import date

from flask import Blueprint

from init import db, bcrypt
from models.user import User
from models.game import Game
from models.platform import Platform
from models.genre import Genre
from models.user_library import User_library
from models.game_genre import Game_genre
from models.game_platform import Game_platform
from models.library_item import Library_item

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

    user_libraries = [
        User_library(user=users[0]),
        User_library(user=users[1]),
    ]

    db.session.add_all(user_libraries)

    games = [
        Game(
            title="Pokemon Diamond",
            publisher="Nintendo",
            description="Pokemon Diamond is a traditional Pokemon RPG that takes place in a region called Sinnoh. In the Sinnoh region, there are two Pokemon that symbolize the region. They appear in the Sinnoh reigon's myths and old folklore. One is called Dialga, and is said to have the power to control time.",
            release_date=date(2008, 9, 28),
            metacritic_score=85,
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

    genres = [
        Genre(genre_name="Action"),  # God of War
        Genre(genre_name="Adventure"),  # Pokemon Diamond
        Genre(genre_name="Role-Playing"),  # Pokemon Diamond and Pyre
        Genre(genre_name="Simulation"),
        Genre(genre_name="Strategy"),  # Slay The Spire
        Genre(genre_name="Sports"),
        Genre(genre_name="Puzzle"),  # Psychonauts
        Genre(genre_name="Idle"),
        Genre(genre_name="Racing"),
        Genre(genre_name="Fighting"),
        Genre(genre_name="Shooter"),
        Genre(genre_name="MMO"),
        Genre(genre_name="Platformer"),  # Psychonauts
        Genre(genre_name="Music"),
        Genre(genre_name="Horror"),
        Genre(genre_name="Survival"),
        Genre(genre_name="Battle Royale"),
        Genre(genre_name="Visual Novel"),
        Genre(genre_name="Rhythm"),
        Genre(genre_name="Roguelike"),  # Slay The Spire, Balatro
        Genre(genre_name="Educational"),
        Genre(genre_name="Card & Board Game"),  # Balatro
        Genre(genre_name="MOBA"),
        Genre(genre_name="Point & Click"),
        Genre(genre_name="Sandbox"),
        Genre(genre_name="Tower Defense"),
        Genre(genre_name="Text Adventure"),
        Genre(genre_name="Hack and Slash"),  # God of War
        Genre(genre_name="Stealth"),
        Genre(genre_name="Flight Simulation"),
        Genre(genre_name="Narrative"),
        Genre(genre_name="Fantasy"),  # God of War
        Genre(genre_name="Indie"),  # Balatro
        Genre(genre_name="Mythology"),  # God of War
        Genre(genre_name="Tactical"),  # Slay the Spire, Balatro
        Genre(genre_name="Party"),
        Genre(genre_name="Turn-Based"),  # Slay the Spire
        Genre(genre_name="Action RPG"),
        Genre(genre_name="Deck Building"),  # Slay the Spire, Balatro
        Genre(genre_name="Open World"),
    ]

    db.session.add_all(genres)

    game_genres = [
        Game_genre(game=games[0], genre=genres[0]),
        Game_genre(game=games[0], genre=genres[1]),
        Game_genre(game=games[0], genre=genres[2]),
        Game_genre(game=games[1], genre=genres[1]),
    ]

    db.session.add_all(game_genres)

    platforms = [
        Platform(platform_name="Windows", platform_type="PC"),
        Platform(platform_name="Linux", platform_type="PC"),
        Platform(platform_name="Mac OS", platform_type="PC"),
        Platform(platform_name="PlayStation Vita", platform_type="Handheld"),
        Platform(platform_name="Nintendo DS", platform_type="Handheld"),
        Platform(platform_name="Nintendo 3DS", platform_type="Handheld"),
        Platform(platform_name="Sega Genesis", platform_type="Home Console"),
        Platform(platform_name="PlayStation 3", platform_type="Home Console"),
        Platform(platform_name="PlayStation 4", platform_type="Home Console"),
        Platform(platform_name="PlayStation 5", platform_type="Home Console"),
        Platform(platform_name="Xbox 360", platform_type="Home Console"),
        Platform(platform_name="Xbox One", platform_type="Home Console"),
        Platform(platform_name="Xbox Series X", platform_type="Home Console"),
        Platform(platform_name="Xbox Series S", platform_type="Home Console"),
        Platform(platform_name="Nintendo 64", platform_type="Home Console"),
        Platform(platform_name="Nintendo Wii", platform_type="Home Console"),
        Platform(platform_name="Nintendo Wii U", platform_type="Home Console"),
        Platform(platform_name="Nintendo Switch", platform_type="Hybrid"),
    ]

    db.session.add_all(platforms)

    game_platforms = [
        Game_platform(game=games[0], platform=platforms[0]),
        Game_platform(game=games[0], platform=platforms[1]),
        Game_platform(game=games[1], platform=platforms[0]),
        Game_platform(game=games[2], platform=platforms[1]),
        Game_platform(game=games[2], platform=platforms[2]),
    ]

    db.session.add_all(game_platforms)

    library_entries = [
        Library_item(
            user_library=user_libraries[1],
            game=games[1],
            status="On-Hold",
            score="80",
        ),
        Library_item(
            user_library=user_libraries[0],
            game=games[0],
            status="On-Hold",
        ),
        Library_item(
            user_library=user_libraries[0],
            game=games[1],
            status="Playing",
            score="75",
        ),
    ]

    db.session.add_all(library_entries)

    db.session.commit()

    print("Tables have been seeded")


@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("All tables have been dropped")


@db_commands.cli.command("refresh")
def create_tables():
    db.drop_all()
    db.create_all()
    print("Tables have been recreated")
