from app import app, db
from app.models import Games, Players
from flask import render_template, request, jsonify, abort, redirect
import app.utils as utils
from sqlalchemy.orm.attributes import flag_modified



@app.route("/")
def index():
    return render_template("index.html", active="home", running=app.running,
                           name=app.tournament_name, master=app.master_name)


@app.route("/cleanup")
def cleanup():
    utils.cleanup()
    return render_template("cleanup.html")


@app.route("/players")
def players_main_view():
    players = Players.query.all()
    return render_template("players_main_view.html", active="players",
                           players=players)


@app.route("/players/autocomplete.json")
def players_autocomplete():
    snippet = request.args.get("q", default="None")
    if snippet is None:
        players = Players.query.with_entities(Players.name).all()
    else:
        players = Players.query.filter(Players.name.contains(snippet)
                                       ).with_entities(Players.name).all()
    return jsonify([str(name[0]) for name in players])


@app.route("/games")
@app.route("/games/<int:page>")
def games_main_view(page=1):
    viewoption = request.args.get("viewoption", default="current")
    if viewoption == "current":
        games = Games.query.filter_by(state=1).paginate(page, per_page=30)
        btn_active = "current"
    elif viewoption == "all":
        games = Games.query.paginate(page, per_page=30)
        btn_active = "all"
    else:
        games = Games.query.filter_by(state=1).paginate(page, per_page=30)
        btn_active = "current"
    game_creation = (len(Players.query.all()) >= 2)
    return render_template("games.html", active="games", games=games,
                           game_creation=game_creation, btn_active=btn_active)


@app.route("/game/create", methods=["POST"])
def create_game():
    if "player2" in request.form.keys() and "player1" in request.form.keys():
        player1 = Players.query.filter_by(name=request.form["player1"]).first_or_404()
        player2 = Players.query.filter_by(name=request.form["player2"]).first_or_404()
        game = utils.create_game(player1, player2, flush=True)
        return jsonify({"id": game.id})
    else:
        return abort(400)


@app.route("/game/delete", methods=["POST"])
def delete_game():
    if "game_id" in request.form.keys():
        game = Games.query.get_or_404(request.form["game_id"])
        utils.delete_game(game)
        return jsonify({"id": request.form["game_id"], "status": "deleted"})
    else:
        return abort(400)


@app.route("/game/end", methods=["POST"])
def end_game():
    if "game_id" in reques.form.keys():
        game = Games.query.get_or_404(request.form["game_id"])
        game = utils.end_game(game, flush=True)
        return jsonify({"id": game.id, "state": game.state})
    else:
        return abort(400)


@app.route("/games/view/<int:id>")
def view_game(id):
    game = Games.query.get_or_404(id)
    states = [{"value": 1, "state": "running", "active": False},
              {"value": 2, "state": "ready", "active": False},
              {"value": 3, "state": "paused", "active": False},
              {"value": 0, "state": "finished", "active": False}]
    [states[i].__setitem__("active", True) for i in range(len(states))
     if states[i]["value"] == game.state]
    return render_template("game_view.html",  active="games", states=states,
                           game=game)


@app.route("/games/create-game")
@app.route("/games/create-game/<method>")
def create_game_select(method="selection"):
    appendix = {}
    if method == "selection":
        if len(Players.query.all()) < 2:
            return render_template("create_game_select.html",
                                   acive="games", avaliable=False)
        return render_template("create_game_select.html",
                               active="games", avaliable=True)
    elif method == "unpaired":
        appendix["player1"], appendix["player2"] = Games.find_pair()
        parsed = "Switzer System"
    elif method == "find-opponent":
        parsed = "Find Opponent"
        player1 = request.args.get("player", default=None)
        opponent = request.args.get("opponent", default=None)
        if player1 is None:
            method = "find-opponent-input"
        else:
            player1 = Players.query.filter_by(name=player1).first_or_404()
            appendix["player1"], appendix["player2"] = Games.find_pair(player1, exceptions=[opponent])
    elif method == "pre-defined":
        parsed = "Pre Defined"
    else:
        print(method)
        return render_template("create_game_select.html", active="games")
    return render_template("create_game_methods.html", active="games",
                           method=method, method_parsed=parsed,
                           appendix=appendix)


@app.route("/tournament/create")
def create_tournament():
    appendix = {}
    step = request.args.get("step", default=1.0, type=float)
    if step == 2.0:
        name = request.args.get("name", default=None)
        app.tournament_name = name
    elif step == 3.0:
        name = request.args.get("name", default=None)
        app.master_name = name
    elif step == 4:
        appendix["name"] = app.tournament_name
        appendix["master"] = app.master_name
        app.running = True
        if request.args.get("add_players", default=False) == "true":
            return redirect("/players/add-players")
    return render_template("create_tournament.html",
                           step=step, active="settings", appendix=appendix)


@app.route("/player/create", methods=["POST"])
def add_player():
    player_dict = utils.add_player(request.form["name"])
    return jsonify(player_dict)


@app.route("/player/delete")
def delete_player():
    return jsonify(utils.remove_player(request.args.get("name")))


@app.route("/player/view/<int:id>")
def player_view(id):
    return render_template("player_view.html", active="players",
                           player=Players.query.get_or_404(id))


@app.route("/players/add-players")
def add_players():
    return render_template("add_players.html", active="players")


@app.route("/settings")
def settings():
    return render_template("settings.html", tournament_name=app.tournament_name,
                           active="settings", master=app.master_name)


@app.route("/settings/changeauth")
def change_auth():
    active = request.args.get("active", default=None)
    pwd = request.args.get("password", default=None)
    name = request.args.get("name", default=None)
    force = request.args.get("force", default=None)
    if pwd is None and name is None and force is None and active is None:
        return abort(400)
    if pwd == "":
        pwd = None
    if name == "":
        name = None
    if force == "on":
        app.config["BASIC_AUTH_FORCE"] = True
    elif force == "off":
        app.config["BASIC_AUTH_FORCE"] = False
    if pwd is not None and pwd != app.config["BASIC_AUTH_PASSWORD"]:
        app.config["BASIC_AUTH_PASSWORD"] = pwd
    if name is not None and name != app.config["BASIC_AUTH_USERNAME"]:
        app.config["BASIC_AUTH_USERNAME"] = name
    if active == "on":
        app.config["BASIC_AUTH_ACTIVE"] = True
    elif active == "off":
        app.config["BASIC_AUTH_ACTIVE"] = False
    utils.save_enviroment()
    return redirec("/settings")


@app.route("/game/update", methods=["POST"])
def update_game_data():
    if "data[0][id]" in request.form and "game_id" in request.form:
        data = []
        keys = ["id", "points"]
        data_steps = int((len(request.form))/2) - 1
        for i in range(data_steps):
            data.append({})
            for key in keys:
                data[i][key] = request.form[f"data[{i}][{key}]"]
        game = Games.query.get_or_404(int(request.form["game_id"]))
        results = game.result
        for new_result in data:
            for i in range(len(results)):
                if results[i]["player_id"] == int(new_result["id"]):
                    results[i]["points"] = new_result["points"]
                    break
        game.result = results
        flag_modified(game, "result")
        game.state = int(request.form["state"])
        db.session.merge(game)
        db.session.flush()
        db.session.commit()
        return jsonify({"game_id": game.id, "result": game.result})
    else:
        return abort(400)


@app.route("/settings/changename")
def changetournamentname():
    name = request.args.get("name", default=None)
    tname = request.args.get("TournamentName", default=None)
    if name is None and tname is None:
        return abort(400)
    elif name is None:
        app.tournament_name = name
    else:
        app.tournament_name = name
    return jsonify({"status": "success", "name": name})


@app.route("/settings/changemaster")
def changemastername():
    name = request.args.get("name", default=None)
    if name is None:
        return abort(400)
    else:
        app.master_name = name
    return jsonify({"status": "success", "name": name})


@app.route("/leaderboard")
def leaderboard():
    limit = request.args.get("limit", default=100, type=int)
    players = Players.get_leaderboard(limit)
    return render_template("leaderboard.html", active="leaderboard",
                           players=players)


@app.route("/about")
def about():
    return render_template("about.html", active="about")
