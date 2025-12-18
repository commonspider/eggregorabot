import os

from dotenv import load_dotenv

from eggregorabot import set_webhook

load_dotenv()
url = os.environ["FLASK_TELEGRAM_WEBHOOK"] + "/" + os.environ["FLASK_TELEGRAM_TOKEN"]
print(url)
result = set_webhook(url=url)
print(result)
