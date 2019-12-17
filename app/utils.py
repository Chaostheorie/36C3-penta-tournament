from app import app, db
from app.models import Players
import json


def setenvvar(**kwargs):
    with open("settings.json") as f:
        settings = json.load(f)
    for key, val in kwargs:
        settings[key] = val
    with open("settings.json", "w") as f:
        json.dump(settings)


def cleanup():
    """Cleanup all existing files"""
    with open("games.json", "w+") as f:
        f.write("[]")
    with open("players.json", "w+") as f:
        f.write("[]")
    with open("settings.json", "w+") as f:
        f.write("[]")


def add_player(name):
    player = Players(name=name)
    db.session.add(player)
    db.session.flush()
    return player


def load_preenv():
    with open("preenv.json", "r") as f:
        preenv = json.load(f)
        print("Preenv: ", preenv)
        for key, val in preenv.items():
            app.__setattr__(key, val)
    return
