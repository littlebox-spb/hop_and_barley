"""
Модуль корзины для управления товарами в сессии пользователя.
"""
from decimal import Decimal
from typing import Dict

from django.conf import settings

from products.models import Product


class Cart:
    """
    Класс для управления корзиной покупок в сессии Django.

    Корзина хранится в сессии и содержит товары с их количеством.
    Формат: {product_id: {'quantity': int, 'price': str}}
    """

    def __init__(self, request):
        """
        Инициализация корзины из сессии.

        Args:
            request: HTTP запрос с доступом к сессии
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # Создаём пустую корзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product: Product, quantity: int = 1, override_quantity: bool = False) -> Dict[str, str]:
        """
        Добавить товар в корзину или обновить его количество.

        Args:
            product: Объект Product для добавления
            quantity: Количество для добавления
            override_quantity: Если True, заменить количество, иначе добавить

        Returns:
            Dict с результатом операции: {'status': 'success/error', 'message': str}
        """
        product_id = str(product.id)

        # Проверка наличия товара на складе
        if quantity > product.stock:
            return {
                'status': 'error',
                'message': f'Available stock: {product.stock}. Cannot add {quantity} items.'
            }

        if product_id not in self.cart:
            # Добавляем новый товар
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if override_quantity:
            # Заменяем количество
            new_quantity = quantity
        else:
            # Добавляем к существующему
            new_quantity = self.cart[product_id]['quantity'] + quantity

        # Проверка общего количества
        if new_quantity > product.stock:
            return {
                'status': 'error',
                'message': f'Cannot add more. Maximum available: {product.stock}'
            }

        self.cart[product_id]['quantity'] = new_quantity
        self.save()

        return {
            'status': 'success',
            'message': f'{product.name} added to cart'
        }

    def remove(self, product: Product) -> None:
        """
        Удалить товар из корзины.

        Args:
            product: Объект Product для удаления
        """
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product: Product, quantity: int) -> Dict[str, str]:
        """
        Обновить количество товара в корзине.

        Args:
            product: Объект Product для обновления
            quantity: Новое количество

        Returns:
            Dict с результатом операции
        """
        if quantity <= 0:
            self.remove(product)
            return {
                'status': 'success',
                'message': 'Item removed from cart'
            }

        return self.add(product, quantity, override_quantity=True)

    def save(self) -> None:
        """Сохранить корзину в сессии и пометить сессию как изменённую."""
        self.session.modified = True

    def clear(self) -> None:
        """Очистить корзину."""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        """
        Итерация по товарам в корзине.

        Yields:
            Dict с информацией о товаре: product, quantity, price, total_price
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self) -> int:
        """
        Получить общее количество товаров в корзине.

        Returns:
            Общее количество всех товаров
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self) -> Decimal:
        """
        Рассчитать общую стоимость корзины.

        Returns:
            Decimal с общей суммой
        """
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def get_items_count(self) -> int:
        """
        Получить количество уникальных товаров в корзине.

        Returns:
            Количество различных товаров
        """
        return len(self.cart)
