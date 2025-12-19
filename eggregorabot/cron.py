import time
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime

from sqlalchemy import select, and_

from .aggregators import aggregator_names, wrap_aggregator
from .app import get_allowed_chat_id, get_db
from .item import Item, send_item
from .models import FeedItem


def cron_job():
    try:
        with ThreadPoolExecutor() as executor:
            for items in executor.map(lambda agg: agg(), map(wrap_aggregator, aggregator_names())):
                for item in items:
                    sent = accept_item(item)
                    if sent:
                        time.sleep(1)
    except Exception as exc:
        print(exc)
    finally:
        return ""


def accept_item(item: Item):
    chat_id = get_allowed_chat_id()
    db = get_db()
    if db.execute(
        select(FeedItem)
        .where(and_(
            FeedItem.chat_id == chat_id,
            FeedItem.source == item["source"],
            FeedItem.item_id == item["id"]
        ))
    ).first() is not None:
        return False
    db.add(FeedItem(
        chat_id=chat_id,
        source=item["source"],
        item_id=item["id"],
        timestamp=datetime.now().timestamp()
    ))
    db.commit()
    send_item(chat_id=chat_id, item=item)
    return True
