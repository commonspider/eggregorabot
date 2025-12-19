import os

from dotenv import load_dotenv

from eggregorabot import create_app, load_aggregators, cron_job, flask_update_endpoint

load_dotenv()
load_aggregators()
app = create_app()
app.route(f"/cronjob")(cron_job)
app.route(f"/{os.environ["FLASK_TELEGRAM_TOKEN"]}", methods=["POST"])(flask_update_endpoint)


@app.route("/")
def index():
    return "OK"


if __name__ == "__main__":
    app.run()
