from dotenv import load_dotenv

from eggregorabot import cron_job, load_aggregators, app_context

load_dotenv()
load_aggregators()

with app_context():
    cron_job()
