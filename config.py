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

    # Secret key for sessions please change it before using
    SECRET_KEY = os.environ["SECRET_KEY"]

    # Database Url
    # Default is a file based sqlite3 databse in the static/databse folder
    try:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    except KeyError:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir,
                                                              "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Basedir
    BASEDIR = basedir

    # auth
    USEENV = os.getenv("USEENV") or False
    BASIC_AUTH_ACTIVE = os.getenv("BASIC_AUTH_ACTIVE") or False
    BASIC_AUTH_FORCE = os.getenv("BASIC_AUTH_FORCE") or False
    BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME") or ""
    BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD") or ""
