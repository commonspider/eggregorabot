from contextlib import contextmanager

from flask import Flask, current_app, g
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .telegram import Telegram


def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    app.config["TELEGRAM"] = Telegram(
        token=app.config["TELEGRAM_TOKEN"],
        default_chat_id=app.config.get("TELEGRAM_DEFAULT_CHAT_ID")
    )
    return app


@contextmanager
def app_context():
    try:
        current_app.config
    except RuntimeError:
        app = create_app()
        with app.app_context(), app.test_request_context():
            yield
    else:
        yield


def get_allowed_chat_id() -> int:
    return current_app.config["TELEGRAM_DEFAULT_CHAT_ID"]


def get_telegram() -> Telegram:
    return current_app.config["TELEGRAM"]


def get_database():
    if 'database' not in g:
        g.database = create_engine(current_app.config["DATABASE"])
    return g.database


def get_db():
    if 'db_session' not in g:
        g.db_session = Session(get_database())
    return g.db_session
