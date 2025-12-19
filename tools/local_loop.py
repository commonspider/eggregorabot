from dotenv import load_dotenv

from eggregorabot import get_telegram, load_aggregators, parse_update, app_context

load_dotenv()
load_aggregators()

with app_context():
    telegram = get_telegram()
    telegram.delete_webhook()
    for update in telegram.loop_updates():
        parse_update(update)
