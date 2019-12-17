from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from json.decoder import JSONDecodeError
from config import config


app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
app.tournament_name = ""
app.master_name = ""
app.running = False

from app.models import *
db.create_all()


from app.utils import load_preenv
try:
    load_preenv()
except JSONDecodeError:
    print("Skipped Preenv loading")

from app.routes import *
from app.filters import *
