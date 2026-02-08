import logging
import threading

logger = logging.getLogger("orders.email")


def run_async(func, *args, **kwargs):
    """
    Запускает функцию в отдельном потоке.
    Используется ТОЛЬКО для I/O (email).
    """

    def wrapper():
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
