"""Views for the reviews app."""

from typing import cast

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from products.models import Product
from users.models import User

from .forms import ReviewForm
from .models import Review


@login_required
@require_POST
def add_review(request: HttpRequest, product_id: int) -> HttpResponse:
    """Add a review for a product."""
    product = get_object_or_404(Product, id=product_id)
    user = cast("User", request.user)

    # защита от повторного отзыва
    if Review.objects.filter(product=product, user=user).exists():
        return redirect(product.get_absolute_url())

    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.user = user
        review.save()

    return redirect(product.get_absolute_url())
