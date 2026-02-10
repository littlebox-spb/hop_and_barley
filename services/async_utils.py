"""Ассинхронное выполнение задач."""

import logging
import threading
from collections.abc import Callable
from typing import Any

logger = logging.getLogger("orders.email")


def run_async(func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
    """Запускает функцию в отдельном потоке."""

    def wrapper() -> None:
        try:
            func(*args, **kwargs)
        except Exception as exc:
            logger.error(
                "Async task failed: %s",
                exc,
                exc_info=True,
            )

    thread = threading.Thread(target=wrapper, daemon=True)
    thread.start()
