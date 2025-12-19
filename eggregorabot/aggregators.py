import importlib.util
import inspect
import sys
from collections.abc import Callable
from pathlib import Path

from flask import current_app

from .item import Item

aggregators: dict[str, Callable[[], list[Item]]] = {}


def load_aggregators(*paths: Path):
    root = Path(__file__).parent.parent

    folders = [
        root / name
        for name in ("private_aggregators", "public_aggregators", *paths)
        if (root / name).exists()
    ]

    for path in folders:
        for file in path.iterdir():
            if not file.is_file() or file.suffix != ".py":
                continue
            spec = importlib.util.spec_from_file_location(file.stem, file)
            module = importlib.util.module_from_spec(spec)
            sys.modules[file.stem] = module
            spec.loader.exec_module(module)


def aggregator(function):
    aggregators[function.__name__] = function
    return aggregators[function.__name__]


def aggregator_names():
    return list(aggregators.keys())


def call_aggregator(name: str):
    if (agg := aggregators.get(name)) is None:
        raise RuntimeError("Aggregator not found")
    kwargs = {
        name: current_app.config.get(f"{aggregator.__name__}_{name}".upper())
        for name in inspect.signature(aggregator).parameters.keys()
    }
    print(kwargs)
    return agg(**kwargs)
