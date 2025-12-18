import os

from dotenv import load_dotenv

from eggregorabot import create_app, load_aggregators, cron_job, receive_update

load_dotenv()
load_aggregators()
app = create_app()
app.route(f"/cronjob")(cron_job)
app.route(f"/{os.environ["FLASK_TELEGRAM_TOKEN"]}")(receive_update)


@app.route("/")
def index():
    return "OK"


if __name__ == "__main__":
    app.run()
