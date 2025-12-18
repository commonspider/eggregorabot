import os

from dotenv import load_dotenv

from eggregorabot import set_webhook

load_dotenv()
result = set_webhook(url=os.environ["FLASK_TELEGRAM_WEBHOOK"] + "/" + os.environ["FLASK_TELEGRAM_TOKEN"])
print(result)
