"""Контекстные процессоры для корзины."""

# Делают информацию о корзине доступной во всех шаблонах.

from django.http import HttpRequest

from .cart import Cart


def cart(request: HttpRequest) -> dict[str, Cart]:
    """
    Добавляет объект корзины в контекст всех шаблонов.

    Args:
        request: HTTP запрос

    Returns:
        Dict с объектом корзины

    """
    return {"cart": Cart(request)}
