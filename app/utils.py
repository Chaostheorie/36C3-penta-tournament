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
    db.session.commit()
    db.session.flush()
    return {"id": player.id, "name": player.name}


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


def create_game(player1, player2, flush=False):
    from app.models import Games, PlayersGames
    g = Games(result=[{"player_id": player1.id, "points": 0},
                      {"player_id": player2.id, "points": 0}])
    db.session.add(g)
    db.session.flush()
    pg1 = PlayersGames(player_id=player1.id, game_id=g.id)
    pg2 = PlayersGames(player_id=player2.id, game_id=g.id)
    db.session.add(pg1)
    db.session.add(pg2)
    db.session.commit()
    if flush:
        db.session.flush()
    return g


def load_enviroment():
    from app.models import Enviroment
    vars = Enviroment.query.all()
    for item in vars:
        if item.type == 0:
            app.__setattr__(item.key, item.val["val"])
        elif item.type == 1:
            app.config[item.key] = item.val["val"]


def save_enviroment():
    from app.models import Enviroment
    keys = ["running", "master_name", "tournament_name"]
    for key in keys:
        envvar = Enviroment.query.filter_by(key=key).first()
        if envvar is None:
            db.session.add(Enviroment(key=key, type=0,
                                      val={"val": app.__getattribute__(key)}))
        else:
            envvar.val["val"] = app.__getattribute__(key)
        db.session.commit()
    keys = ["BASIC_AUTH_FORCE", "BASIC_AUTH_PASSWORD",
            "BASIC_AUTH_USERNAME", "BASIC_AUTH_ACTIVE"]
    for key in keys:
        if envvar is None:
            db.session.add(Enviroment(key=key, type=1,
                                      val={"val": app.config[key]}))
        else:
            envvar.val["val"] = app.config[key]
        db.session.commit()


def dump_enviroment():
    import json
    from app.models import Enviroment
    with open("preenv.json", "w+") as f:
        json.dump([{"key": envvar.key, "val": envvar.val}
                   for envvar in Enviroment.query.all()])
