# admin_panel/views.py
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.db.models import Sum, Count
from django.urls import reverse_lazy

from products.models import Category, Product
from orders.models import Order
from users.models import User
from .mixins import StaffRequiredMixin
from .forms import ProductAdminForm
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.text import slugify


class AdminDashboardView(StaffRequiredMixin, TemplateView):
    template_name = "admin/dashboard.html"

    def get_context_data(self, **kwargs):
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


class AdminProductListView(StaffRequiredMixin, ListView):
    model = Product
    template_name = "admin/products.html"
    context_object_name = "products"
    paginate_by = 10
    ordering = "name"


import uuid
from pathlib import Path
from django.conf import settings


class AdminProductCreateView(StaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductAdminForm
    template_name = "admin/add.html"
    success_url = reverse_lazy("admin_products")

    def form_valid(self, form):
        product = form.save(commit=False)

        # ✅ ГЕНЕРАЦИЯ SLUG
        base_slug = slugify(product.name)
        slug = base_slug
        counter = 1

        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        product.slug = slug

        image = self.request.FILES.get("picture")

        if image:
            ext = image.name.split(".")[-1].lower()
            filename = f"{uuid.uuid4()}.{ext}"

            # 👉 static/img/product/
            static_path = Path(settings.BASE_DIR) / "static" / "img" / "products"
            static_path.mkdir(parents=True, exist_ok=True)

            file_path = static_path / filename

            with open(file_path, "wb+") as f:
                for chunk in image.chunks():
                    f.write(chunk)

            # 👉 сохраняем относительный путь
            form.instance.picture_url = f"img/products/{filename}"

        return super().form_valid(form)


class AdminProductUpdateView(StaffRequiredMixin, UpdateView):
    model = Product
    form_class = ProductAdminForm
    template_name = "admin/add.html"
    success_url = reverse_lazy("admin_products")

    def form_valid(self, form):
        # 🔥 берём объект вручную
        product = form.save(commit=False)

        image = self.request.FILES.get("picture")

        # если загружают новую картинку
        if image:
            # 🧹 удалить старую
            if product.picture_url:
                old_path = Path(settings.BASE_DIR) / "static" / product.picture_url
                if old_path.exists():
                    old_path.unlink()

            ext = image.name.split(".")[-1].lower()
            filename = f"{uuid.uuid4()}.{ext}"

            static_path = Path(settings.BASE_DIR) / "static" / "img" / "products"
            static_path.mkdir(parents=True, exist_ok=True)

            file_path = static_path / filename
            with open(file_path, "wb+") as f:
                for chunk in image.chunks():
                    f.write(chunk)

            product.picture_url = f"img/products/{filename}"

        # 💾 СОХРАНЯЕМ ВСЁ ЯВНО
        product.save()

        return redirect(self.success_url)


class AdminCategoryCreateView(StaffRequiredMixin, CreateView):
    model = Category
    fields = ["name"]
    success_url = reverse_lazy("admin_product_add")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.slug = slugify(category.name)

        if Category.objects.filter(slug=category.slug).exists():
            messages.error(self.request, "Category already exists.")
            return redirect(self.success_url)

        category.save()
        messages.success(self.request, "Category added.")
        return redirect(self.success_url)


class AdminCategoryDeleteView(StaffRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy("admin_products")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if Product.objects.filter(category=self.object).exists():
            messages.error(request, "Cannot delete category with assigned products.")
            return redirect(self.success_url)

        return super().delete(request, *args, **kwargs)
