from dotenv import load_dotenv

from eggregorabot import cron_job, load_aggregators

load_dotenv()
load_aggregators()
cron_job()
