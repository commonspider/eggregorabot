from typing import TypedDict, NotRequired

from .app import get_telegram


class Item(TypedDict):
    source: str
    id: str
    name: str
    description: NotRequired[str]
    html: NotRequired[str]
    link: NotRequired[str]
    event_type: NotRequired[str]
    tags: NotRequired[list[str]]
    location: NotRequired[str]
    latitude: NotRequired[float]
    longitude: NotRequired[float]
    start_date: NotRequired[str]
    start_time: NotRequired[str]
    end_date: NotRequired[str]
    end_time: NotRequired[str]



def send_item(*, chat_id: int | str = None, item: Item):
    return get_telegram().send_message(
        chat_id=chat_id,
        text=format_item(item)
    )


def format_item(item: Item):
    return f"""{item["name"]}
{item.get("description", "")}
Source: {item["source"]}"""
