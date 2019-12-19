import os
import json
from json.decoder import JSONDecodeError

# Load data from .env file if avaible
from dotenv import load_dotenv
load_dotenv()

# Config for basedir
basedir = os.path.abspath(os.path.dirname(__file__))


def check_preenv(key):
    with open("preenv.json", "r+") as f:
        try:
            preenv = json.load(f)
        except JSONDecodeError:
            print("Preenv skipped")
        if isinstance(key, list):
            if len([item for item in key if key not in preenv.keys()]) > 0:
                return False
        else:
            if key not in preenv.keys():
                return False
        return True


def load_preenv(key):
    with open("preenv.json") as f:
        preenv = json.load(f)
    return preenv[key]


class config(object):
    # App infos
    APP_VERSION = "Experimental"
    APP_NAME = "36C3 Edition Penta-Tournament"
    APP_LOCAL = "en"
    LOAD_PREENV = True

    # SQLAlchemy Settings
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI") or \
        "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Basedir
    BASEDIR = basedir


class BasicAuthConfig(config):
    BASIC_AUTH_PASSWORD = (check_preenv("password") and load_preenv("password")) \
                         or os.urandom(36)
    BASIC_AUTH_USERNAME = (check_preenv("username") and load_preenv("username")) \
                         or os.urandom(36)
    BASIC_AUTH_FORCE = (check_preenv("force") and load_preenv("force")) \
                      or True
