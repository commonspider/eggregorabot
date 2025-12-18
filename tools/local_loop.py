from dotenv import load_dotenv

from eggregorabot import loop_updates, load_aggregators, parse_update

load_dotenv()
load_aggregators()

for update in loop_updates():
    parse_update(update)
