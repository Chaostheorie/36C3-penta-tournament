import atexit
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from config import config


app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
app.tournament_name = ""
app.master_name = ""
app.running = False

from app.models import *
db.create_all()


import app.utils as utils
if app.config["LOAD_ENVIROMENT"]:
    utils.load_enviroment(without_auth=app.config["USEENV"])
if app.config["SAVE_ENVIROMENT"]:
    atexit.register(utils.save_enviroment)


if app.config["BASIC_AUTH_ACTIVE"]:
    auth = BasicAuth(app)

from app.routes import *
from app.filters import *
