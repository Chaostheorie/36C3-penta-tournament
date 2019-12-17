import os

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

    # SQLAlchemy Settings
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI") or \
        "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Basedir
    BASEDIR = basedir
