import os

from sqlalchemy.engine.url import URL


class Configuration(object):
    ###################################
    # FLASK CONFIG
    SECRET_KEY = "Yjlaskdfjloiasdfh"

    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

    JSON_SORT_KEYS = False

    ###################################
    # FLASK-SQLALCHEMY CONFIG
    SQLALCHEMY_DATABASE_URI = URL.create(
        "postgresql",
        username=os.environ.get("DATABASE_USER"),
        password=os.environ.get("DATABASE_PASSWORD"),
        host=os.environ.get("DATABASE_HOST"),
        port=os.environ.get("DATABASE_PORT"),
        database=os.environ.get("DATABASE_DB"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = os.environ.get("SQLALCHEMY_RECORD_QUERIES", False)
