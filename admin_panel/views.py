# admin_panel/views.py
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.db.models import Sum, Count
from django.urls import reverse_lazy

from products.models import Category, Product
from orders.models import Order
from users.models import User
from .mixins import StaffRequiredMixin
from .forms import ProductAdminForm


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


class AdminProductCreateView(StaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductAdminForm
    template_name = "admin/add.html"
    success_url = reverse_lazy("admin_products")


class AdminProductUpdateView(StaffRequiredMixin, UpdateView):
    model = Product
    form_class = ProductAdminForm
    template_name = "admin/add.html"
    success_url = reverse_lazy("admin_products")


class AdminCategoryCreateView(StaffRequiredMixin, CreateView):
    model = Category
    fields = ["name", "slug"]
    success_url = reverse_lazy("admin_products")
