"""Admin panel views."""

import json
import uuid
from pathlib import Path
from typing import TYPE_CHECKING, Any

from django.conf import settings
from django.db.models import Sum
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views import View
from django.views.generic import (
    CreateView,
    ListView,
    TemplateView,
    UpdateView,
)
from unidecode import unidecode

from orders.models import Order
from products.models import Category, Product
from users.models import User

from .forms import ProductAdminForm
from .mixins import StaffRequiredMixin

if TYPE_CHECKING:
    ProductAdminList = ListView[Product]
    ProductAdminCreate = CreateView[Product, ProductAdminForm]
    ProductAdminUpdate = UpdateView[Product, ProductAdminForm]
    CategoryAdminCreate = CreateView[Category, Any]
else:
    ProductAdminCreate = CreateView
    ProductAdminList = ListView
    ProductAdminUpdate = UpdateView
    CategoryAdminCreate = CreateView


class AdminDashboardView(StaffRequiredMixin, TemplateView):
    """Admin dashboard view."""

    template_name = "admin/dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get context data for the admin dashboard view."""
        ctx = super().get_context_data(**kwargs)

        ctx["total_sales"] = (
            Order.objects.filter(status="paid").aggregate(total=Sum("total_price"))[
                "total"
            ]
            or 0
        )
        ctx["total_users"] = User.objects.count()
        ctx["total_orders"] = Order.objects.count()
        ctx["pending_orders"] = Order.objects.filter(status="pending").count()

        return ctx


class AdminProductListView(StaffRequiredMixin, ProductAdminList):
    """Admin product list view."""

    model = Product
    template_name = "admin/products.html"
    context_object_name = "products"
    paginate_by = 10
    ordering = "name"


class AdminProductCreateView(StaffRequiredMixin, ProductAdminCreate):
    """Admin product create view."""

    model = Product
    form_class = ProductAdminForm
    template_name = "admin/add.html"
    success_url = reverse_lazy("admin_products")

    def form_valid(self, form: Any) -> HttpResponse:
        """Form valid."""
        product = form.instance
        base_slug = slugify(unidecode(product.name))
        slug = base_slug
        counter = 1

        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        product.slug = slug

        image: Any = self.request.FILES.get("picture")
        if image:
            ext = image.name.split(".")[-1].lower()
            filename = f"{uuid.uuid4()}.{ext}"
            static_path = Path(settings.BASE_DIR) / "static" / "img" / "products"
            static_path.mkdir(parents=True, exist_ok=True)
            file_path = static_path / filename
            with open(file_path, "wb+") as f:
                for chunk in image.chunks():
                    f.write(chunk)
            product.picture_url = f"img/products/{filename}"

        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get context data."""
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.order_by("name")
        return ctx


class AdminProductUpdateView(StaffRequiredMixin, ProductAdminUpdate):
    """Admin product update view."""

    model = Product
    form_class = ProductAdminForm
    template_name = "admin/add.html"
    success_url = reverse_lazy("admin_products")

    def form_valid(self, form: Any) -> HttpResponse:
        """Form valid."""
        product = form.save(commit=False)
        image = self.request.FILES.get("picture")

        if image:
            if product.picture_url:
                old_path = Path(settings.BASE_DIR) / "static" / product.picture_url
                if old_path.exists():
                    old_path.unlink()

            filename = str(image.name)
            ext = filename.split(".")[-1].lower()
            filename = f"{uuid.uuid4()}.{ext}"
            static_path = Path(settings.BASE_DIR) / "static" / "img" / "products"
            static_path.mkdir(parents=True, exist_ok=True)
            file_path = static_path / filename

            with open(file_path, "wb+") as f:
                for chunk in image.chunks():
                    f.write(chunk)

            product.picture_url = f"img/products/{filename}"

        product.save()

        return redirect(self.success_url)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get context data."""
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.order_by("name")
        return ctx


class AdminCategoryCreateView(StaffRequiredMixin, CategoryAdminCreate):
    """Admin category create view."""

    model = Category
    fields = ["name"]

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        """Post method."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        name = data.get("name", "").strip()
        if not name:
            return JsonResponse({"error": "Empty name"}, status=400)
        if not Category.objects.filter(name=name).exists():
            slug = slugify(name)
            if Category.objects.filter(slug=slug).exists():
                return JsonResponse({"error": "Category already exists"}, status=400)

            cat = Category.objects.create(name=name, slug=slug)

        return JsonResponse(
            {
                "id": cat.id,
                "name": cat.name,
            }
        )


class AdminCategoryDeleteView(StaffRequiredMixin, View):
    """Admin category delete view."""

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        """Post method."""
        cat = get_object_or_404(Category, pk=kwargs["pk"])

        if Product.objects.filter(category=cat).exists():
            return JsonResponse({"error": "Category has products"}, status=400)

        cat.delete()
        return JsonResponse({"ok": True})
