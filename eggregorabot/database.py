from flask import g, current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column

from .app import with_app_context


def get_database():
    if 'database' not in g:
        g.database = create_engine(current_app.config["DATABASE"])
    return g.database


def get_db_session():
    if 'db_session' not in g:
        g.db_session = Session(get_database())
    return g.db_session


class Base(DeclarativeBase):
    pass


@with_app_context
def create_database():
    Base.metadata.create_all(get_database())


class AggregatorStatus(Base):
    __tablename__ = "aggregator_status"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int]
    name: Mapped[str]
    status: Mapped[bool]


class FeedItem(Base):
    __tablename__ = "feed_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int]
    source: Mapped[str]
    item_id: Mapped[str]
    timestamp: Mapped[float]
