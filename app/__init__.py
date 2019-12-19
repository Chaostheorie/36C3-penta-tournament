from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from json.decoder import JSONDecodeError
from config import config, BasicAuthConfig


app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
app.use_auth = False
app.tournament_name = ""
app.master_name = ""
app.running = False

from app.models import *
db.create_all()


from app.utils import load_preenv
if app.config["LOAD_PREENV"] is True:
    try:
        load_preenv()
    except JSONDecodeError:
        print("Skipped Preenv loading")

if app.use_auth:
    app.config.from_object(BasicAuthConfig)
    auth = BasicAuth(app)
from app.routes import *
from app.filters import *
