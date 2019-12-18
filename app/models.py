from app import db
import app.utils as utils
from sqlalchemy.sql import func
from operator import itemgetter


class Players(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer(), primary_key="True")
    name = db.Column(db.String(), unique=True)

    def points(self):
        points = 0
        for game in self.games.all():
            if game.winner().id == self.id:
                points += 1
        return points

    @staticmethod
    def get_leaderboard(limit=100):
        players = [{"player": player, "points": player.points()}
                   for player in Players.query.all()]
        players = sorted(players, key=itemgetter("points"), reverse=True)
        return players[:limit]


class Games(db.Model):
    """Table for managing of games"""
    __tablename__ = "games"

    id = db.Column(db.Integer(), primary_key=True)
    result = db.Column(db.JSON())  # [{"player_id": int, "points": int}]
    date = db.Column(db.Date())
    state = db.Column(db.Integer(), server_default="1")

    def active(self):
        """Method for checking game state"""
        if self.state == 1 or self.state == 2 or self.state == 3:
            return True
        else:
            return False

    def parse_state(self):
        states = {1: "running", 2: "ready", 3: "paused", 0: "finished"}
        return states[self.state]

    def get_points(self, player, only_id=True):
        if only_id:
            points = [result["points"] for result in self.result
                      if result["player_id"] == player]
        else:
            points = [result["points"] for result in self.result
                      if result["player_id"] == player.id]
        return points[0]

    players = db.relationship("Players", secondary="players_games",
                              backref=db.backref("games", lazy="dynamic"))

    def winner(self, only_full=False):
        if only_full:
            winner = None
            for player in self.result:
                if player["points"] == 3:
                    winner = player
                    break
            if winner is None:
                return None
        else:
            winner = self.result[0]
            for player in self.result:
                if player["points"] > winner["points"]:
                    winner = player
        for player in self.players:
            if player.id == winner["player_id"]:
                return player
        return None

    @staticmethod
    def unmatched(player1, player2):
        test_statement = PlayersGames.player_id == player1.id or PlayersGames.player_id == player2.id
        test_query = PlayersGames.query.filter(test_statement).all()
        if utils.duplicates_exist(test_query):
            return True
        else:
            return False

    @staticmethod
    def find_pair(player1=None):
        """Find pair """
        if player1 is None:
            player1 = Players.query.order_by(func.random()).first()
        players = [{"player": player, "points": player.points()}
                   for player in Players.query.filter(Players.id != player1.id
                                                      ).all()]
        players = utils.sortin(players, player1, extract=True)
        for player in players:
            if Games.unmatched(player1, player):
                player2 = player
                break
        return player1, player2

    def __repr__(self):
        return f"<game {self.id} from {self.date.strftime('%d.%m.%Y')}>"


class PlayersGames(db.Model):
    __tablename__ = "players_games"

    id = db.Column(db.Integer(), primary_key=True)
    game_id = db.Column(db.Integer(),
                        db.ForeignKey("games.id", ondelete="CASCADE"))
    player_id = db.Column(db.Integer(),
                          db.ForeignKey("players.id", ondelete="CASCADE"))