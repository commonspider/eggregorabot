import time
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime

from sqlalchemy import select, and_

from .aggregators import list_aggregators, get_aggregator
from .app import with_app_context, get_chat_id
from .item import send_item
from .database import FeedItem, get_db_session
from .item import Item


@with_app_context
def cron_job():
    with ThreadPoolExecutor() as executor:
        for items in executor.map(run_aggregator, list_active_aggregators()):
            for item in items:
                sent = accept_item(item)
                if sent:
                    time.sleep(1)


def list_active_aggregators():
    return list_aggregators()


def run_aggregator(name: str) -> list[Item]:
    aggregator = get_aggregator(name)
    return aggregator()


def accept_item(item: Item):
    chat_id = get_chat_id()
    session = get_db_session()
    if session.execute(
        select(FeedItem)
        .where(and_(
            FeedItem.chat_id == chat_id,
            FeedItem.source == item["source"],
            FeedItem.item_id == item["id"]
        ))
    ).first() is not None:
        return False
    session.add(FeedItem(
        chat_id=chat_id,
        source=item["source"],
        item_id=item["id"],
        timestamp=datetime.now().timestamp()
    ))
    session.commit()
    send_item(item)
    return True
