from app import app, db
from itertools import groupby
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
    from app.models import Players
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


def duplicates_exist(list):
    probe = []
    for item in list:
        if item in probe:
            probe.append(item)
        else:
            return False
    return True


def sortin(players, player, extract=False):
    points = player.points()
    players = [i[0] for i in groupby(players)]
    for i in range(len(players)):
        if players[i]["points"] <= points:
            players.insert(0, players[i])
            players.pop(i+1)
        else:
            players.insert(-1, players[i])
            players.pop(i+1)
    if extract:
        return [_player["player"] for _player in players]
    return players
