from decimal import Decimal
from typing import Any

from django.conf import settings

from products.models import Product


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product: Product, quantity: int = 1, override_quantity: bool = False):
        product_id = str(product.id)
        if quantity > product.stock:
            return {
                "status": "error",
                "message": f"Available stock for {product.name} is {product.stock}. Cannot add {quantity} items.",
            }
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}

        if override_quantity:
            new_quantity = quantity
        else:
            new_quantity = self.cart[product_id]["quantity"] + quantity

        if new_quantity > product.stock:
            return {
                "status": "error",
                "message": f"Cannot add more. Maximum available: {product.stock}.",
            }

        self.cart[product_id]["quantity"] = new_quantity
        self.save()

        return {"status": "success", "message": f"{product.name} added to cart."}

    def remove(self, product: Product) -> dict[str, str]:
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

        return {"status": "success", "message": f"{product.name} removed from cart."}

    def update(self, product: Product, quantity: int) -> dict[str, str] | Any:

        if quantity <= 0:
            self.remove(product)
            return {"status": "success", "message": "Item removed from cart."}
        return self.add(product, quantity, override_quantity=True)

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self) -> Decimal:
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def get_items_count(self) -> int:
        return len(self.cart)
