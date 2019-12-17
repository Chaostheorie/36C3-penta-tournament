from app import db
from app.models import Players, Games, PlayersGames
from datetime import date

sample_player = Players(name="Johnson")
db.session.add(sample_player)
db.session.flush()
for i in range(1, 4):
    sample_game = Games(date=date.today(), result=[{"player_id": sample_player.id,
                                                   "points": i}])
    db.session.add(sample_game)
    db.session.flush()
    db.session.add(PlayersGames(player_id=sample_player.id,
                                game_id=sample_game.id))
db.session.commit()
