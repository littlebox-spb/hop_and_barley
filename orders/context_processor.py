"""
Контекстные процессоры для корзины.
Делают информацию о корзине доступной во всех шаблонах.
"""
from .cart import Cart


def cart(request):
    """
    Добавляет объект корзины в контекст всех шаблонов.

    Args:
        request: HTTP запрос

    Returns:
        Dict с объектом корзины
    """
    return {'cart': Cart(request)}
