import inspect
import time
from collections.abc import Callable
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from functools import partial

from flask import current_app
from sqlalchemy import select, and_

from .aggregators import aggregators
from .app import get_allowed_chat_id, get_db
from .item import Item, send_item
from .models import FeedItem


def cron_job():
    with ThreadPoolExecutor() as executor:
        aggregators_ready = [
            partial(aggregator, **get_aggregator_parameters(aggregator))
            for aggregator in aggregators.values()
        ]
        for items in executor.map(lambda agg: agg(), aggregators_ready):
            for item in items:
                sent = accept_item(item)
                if sent:
                    time.sleep(1)


def get_aggregator_parameters(aggregator: Callable[[], list[Item]]):
    return {
        name: current_app.config.get(f"{aggregator.__name__}_{name}".upper())
        for name in inspect.signature(aggregator).parameters.keys()
    }


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
