import os
import json
from json.decoder import JSONDecodeError

# Load data from .env file if avaible
from dotenv import load_dotenv
load_dotenv()

# Config for basedir
basedir = os.path.abspath(os.path.dirname(__file__))


class config(object):
    # App infos
    APP_VERSION = "Experimental"
    APP_NAME = "36C3 Edition Penta-Tournament"
    APP_LOCAL = "en"
    LOAD_ENVIROMENT = True
    SAVE_ENVIROMENT = True

    # SQLAlchemy Settings
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI") or \
        "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Basedir
    BASEDIR = basedir

    # auth
    BASIC_AUTH_ACTIVE = False
    BASIC_AUTH_FORCE = False
    BASIC_AUTH_USERNAME = ""
    BASIC_AUTH_PASSWORD = ""
