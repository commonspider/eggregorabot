import inspect
from functools import wraps
from typing import TypedDict, Any, NotRequired, Literal

from requests import Session


def snake_to_camelcase(value: str):
    [first, *rest] = value.split("_")
    rest = map(lambda x: x.capitalize(), rest)
    return "".join([first, *rest])


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


def api(method):
    @wraps(method)
    def decorator(self, *args, **kwargs):
        if len(args) > 0:
            raise RuntimeError("No positional arguments allowed in Telegram API call")
        if has_chat_id and "chat_id" not in kwargs:
            kwargs["chat_id"] = self._default_chat_id
        return self._request(name, kwargs)

    name = snake_to_camelcase(method.__name__)
    has_chat_id = "chat_id" in inspect.signature(method).parameters
    return decorator


class Telegram:
    def __init__(self, token: str, default_chat_id: int | str = None):
        self._token = token
        self._default_chat_id = default_chat_id
        self._session = Session()

    def _request(self, endpoint: str, parameters: dict[str, Any] = None):
        response = self._session.post(f"https://api.telegram.org/bot{self._token}/{endpoint}", json=parameters)
        content = response.json()
        if not content["ok"]:
            raise Exception(content)
        return content["result"]

    @api
    def get_updates(self, *, offset: int = None) -> list[Update]:
        ...

    def loop_updates(self, *, offset: int = None):
        offset = offset or 0
        while True:
            for update in self.get_updates(offset=offset):
                yield update
                offset = max(offset, update["update_id"] + 1)

    @api
    def set_webhook(self, *, url: str) -> bool:
        ...

    @api
    def delete_webhook(self) -> bool:
        ...

    @api
    def send_message(self, *, chat_id: int | str = None, text: str) -> Message:
        ...

    @api
    def get_chat_administrators(self, *, chat_id: int | str = None) -> list[ChatMember]:
        ...
