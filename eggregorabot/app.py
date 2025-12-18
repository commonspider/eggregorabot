from functools import wraps

from flask import Flask, current_app, g
from requests import Session


def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    return app


def with_app_context(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        try:
            current_app.config
        except RuntimeError:
            app = create_app()
            with app.app_context(), app.test_request_context():
                return function(*args, **kwargs)
        else:
            return function(*args, **kwargs)

    return decorator


def get_session() -> Session:
    if 'session' not in g:
        g.session = Session()
    return g.session


def get_token() -> str:
    return current_app.config["TELEGRAM_TOKEN"]


def get_chat_id() -> int:
    if (chat_id := g.get("chat_id")) is not None:
        return chat_id
    if (debug_chat_id := current_app.config.get("TELEGRAM_CHAT_ID")) is not None:
        return debug_chat_id
    raise ValueError("Parameter chat_id is not set")


def set_chat_id(chat_id: int):
    g.chat_id = chat_id
