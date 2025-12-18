from typing import TypedDict, NotRequired

from .telegram import send_message


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


def send_item(item: Item):
    return send_message(
        text=
f"""{item["name"]}
{item.get("description", "")}
Source: {item["source"]}"""
    )
