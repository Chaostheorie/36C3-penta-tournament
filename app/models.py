from app import db
from operator import itemgetter


class Players(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer(), primary_key="True")
    name = db.Column(db.String())

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

    def winner(self):
        winner = self.result[0]
        for player in self.result:
            if player["points"] > winner["points"]:
                winner = player
        for player in self.players:
            if player.id == winner["player_id"]:
                return player

    def __repr__(self):
        return f"<game {self.id} from {self.date.strftime('%d.%m.%Y')}>"


class PlayersGames(db.Model):
    __tablename__ = "players_games"

    id = db.Column(db.Integer(), primary_key=True)
    game_id = db.Column(db.Integer(),
                        db.ForeignKey("games.id", ondelete="CASCADE"))
    player_id = db.Column(db.Integer(),
                          db.ForeignKey("players.id", ondelete="CASCADE"))
