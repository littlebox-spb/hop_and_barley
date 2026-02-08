from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from products.models import Product

from .forms import ReviewForm
from .models import Review


@login_required
@require_POST
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # защита от повторного отзыва
    if Review.objects.filter(product=product, user=request.user).exists():
        return redirect(product.get_absolute_url())

    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.user = request.user
        review.save()

    return redirect(product.get_absolute_url())
