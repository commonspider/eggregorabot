import json
import time

from flask import request

from .aggregators import list_aggregators, get_aggregator
from .app import with_app_context, get_allowed_chat_id
from .item import send_item
from .telegram import Update, get_chat_administrators, send_message


def receive_update():
    try:
        update = json.loads(request.data.decode())
        parse_update(update)
    except Exception as exc:
        with open("last_exception", "w") as f:
            print(exc, file=f)
    finally:
        return ""



@with_app_context
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
        for admin in get_chat_administrators(chat_id=chat_id):
            if admin["user"]["id"] == user_id:
                break
        else:
            return
        parse_command(command, argument)
        break


def parse_command(command: str, argument: str = None):
    if command == "/lista":
        aggregators = list_aggregators()
        if len(aggregators) == 0:
            send_message("Nessun feed configurato")
        else:
            send_message(text="\n".join(list_aggregators()))
    elif command == "/invia":
        if argument is None:
            send_message(text="Manca il nome del feed")
        elif (aggregator := get_aggregator(argument)) is None:
            send_message(text="Feed non trovato.")
        else:
            items = aggregator()
            if len(items) == 0:
                send_message(text="Il feed è vuoto")
            else:
                for item in items:
                    send_item(item)
                    time.sleep(1)
    else:
        send_message(text="Comando inesistente.")
