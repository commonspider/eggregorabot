from dotenv import load_dotenv

from eggregorabot import initialize_models, app_context

load_dotenv()

with app_context():
    initialize_models()
