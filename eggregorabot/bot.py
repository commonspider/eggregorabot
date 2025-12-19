import json
import time

from flask import request

from .aggregators import aggregators
from .app import get_allowed_chat_id, get_telegram
from .item import send_item
from .telegram import Update


def flask_update_endpoint():
    try:
        update = json.loads(request.data.decode())
        parse_update(update)
    except Exception as exc:
        with open("last_exception", "w") as f:
            print(exc, file=f)
    finally:
        return ""



def parse_update(update: Update):
    if (message := update.get("message")) is None:
        return
    if (user := message.get("from")) is None:
        return
    if message["chat"]["type"] not in ("group", "supergroup"):
        return
    if (chat_id := message["chat"]["id"]) != get_allowed_chat_id():
        return
    user_id = user["id"]

    for entity in message.get("entities", ()):
        if entity["type"] != "bot_command":
            continue
        [command, *rest] = message["text"][entity["offset"]:].split(" ")
        command = command.split("@")[0]
        argument = rest[0] if len(rest) > 0 else None
        for admin in get_telegram().get_chat_administrators(chat_id=chat_id):
            if admin["user"]["id"] == user_id:
                break
        else:
            return
        parse_command(chat_id, command, argument)
        break


def parse_command(chat_id: int, command: str, argument: str = None):
    telegram = get_telegram()
    if command == "/lista":
        if len(aggregators) == 0:
            telegram.send_message(chat_id=chat_id, text="Nessun feed configurato")
        else:
            telegram.send_message(chat_id=chat_id, text="\n".join(aggregators.keys()))
    elif command == "/invia":
        if argument is None:
            telegram.send_message(chat_id=chat_id, text="Manca il nome del feed")
        elif (aggregator := aggregators[argument]) is None:
            telegram.send_message(chat_id=chat_id, text="Feed non trovato.")
        else:
            items = aggregator()
            if len(items) == 0:
                telegram.send_message(chat_id=chat_id, text="Il feed è vuoto")
            else:
                for item in items:
                    send_item(chat_id=chat_id, item=item)
                    time.sleep(1)
    else:
        telegram.send_message(chat_id=chat_id, text="Comando inesistente.")
