from app import app
from app.models import Games, Players
from flask import render_template, request, jsonify, abort
import app.utils as utils


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
    return render_template("players_main_view.html", active="players", players=players)


@app.route("/games")
@app.route("/games/<int:page>")
def games_main_view(page=1):
    games = Games.query.paginate(page, per_page=30)
    return render_template("games.html", active="games",
                           games=games)


@app.route("/user/<int:id>")
def view_game(id):
    return Players.query.get_or_404(id)

@app.route("/game/create")
def create_game():
    return


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
    elif step == 3.5:
        name = request.args.get("name", default=None)
        db.session.add(Players(name=name))
        db.session.commit()
    elif step == 4:
        appendix["name"] = app.tournament_name
        appendix["master"] = app.master_name
        app.running = True
    return render_template("create_tournament.html",
                           step=step, active="settings", appendix=appendix)


@app.route("/player/create")
def add_player():
    player_dict = utils.add_player(request.args.get("name"))
    return jsonify(player_dict)


@app.route("/player/delete")
def delete_player():
    return jsonify(utils.remove_player(request.args.get("name")))


@app.route("/player/<int:id>")
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
