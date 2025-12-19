import os

from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


def initialize_models():
    engine = create_engine(current_app.config["DATABASE"])
    Base.metadata.create_all(engine)


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
