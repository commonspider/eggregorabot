from dotenv import load_dotenv
from flask import current_app

from eggregorabot import app_context, get_telegram

load_dotenv()

with app_context():
    telegram = get_telegram()
    url = current_app.config["TELEGRAM_WEBHOOK"] + "/" + current_app.config["TELEGRAM_TOKEN"]
    result = telegram.set_webhook(url=url)
    print(result)
