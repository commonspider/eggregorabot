import inspect
from functools import wraps
from typing import TypedDict, Any, NotRequired, Literal

from .app import with_app_context, get_session, get_token, get_allowed_chat_id
from .utils import snake_to_camelcase


def request(endpoint: str, parameters: dict[str, Any] = None):
    response = get_session().post(f"https://api.telegram.org/bot{get_token()}/{endpoint}", json=parameters)
    content = response.json()
    if not content["ok"]:
        raise Exception(content)
    return content["result"]


def api(method):
    @wraps(method)
    @with_app_context
    def decorator(*args, **kwargs):
        if len(args) > 0:
            raise RuntimeError("No positional arguments allowed in Telegram API call")
        if has_chat_id and "chat_id" not in kwargs:
            kwargs["chat_id"] = get_allowed_chat_id()
        return request(name, kwargs)

    name = snake_to_camelcase(method.__name__)
    has_chat_id = "chat_id" in inspect.signature(method).parameters
    return decorator


class User(TypedDict):
    id: int


class Chat(TypedDict):
    id: int
    type: Literal["private", "group", "supergroup", "channel"]


class ChatMember(TypedDict):
    user: User


class MessageEntity(TypedDict):
    type: Literal["bot_command"]
    offset: int
    length: int


Message = TypedDict("Message", {
    "from": NotRequired[User],
    "chat": Chat,
    "entities": NotRequired[list[MessageEntity]],
    "text": NotRequired[str]
})


class Update(TypedDict):
    update_id: int
    message: NotRequired[Message]


@api
def get_updates(*, offset: int = None) -> list[Update]:
    ...


def loop_updates(*, offset: int = None):
    offset = offset or 0
    while True:
        for update in get_updates(offset=offset):
            yield update
            offset = max(offset, update["update_id"] + 1)


@api
def set_webhook(*, url: str) -> bool:
    pass


@api
def send_message(*, chat_id: int | str = None, text: str) -> Message:
    ...


@api
def get_chat_administrators(*, chat_id: int | str = None) -> list[ChatMember]:
    pass
