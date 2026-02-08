# admin_panel/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.AdminDashboardView.as_view(), name="admin_dashboard"),
    path("products/", views.AdminProductListView.as_view(), name="admin_products"),
    path(
        "products/add/",
        views.AdminProductCreateView.as_view(),
        name="admin_product_add",
    ),
    path(
        "products/<int:pk>/edit/",
        views.AdminProductUpdateView.as_view(),
        name="admin_product_edit",
    ),
    path(
        "categories/add/",
        views.AdminCategoryCreateView.as_view(),
        name="admin_category_add",
    ),
    path(
        "categories/delete/<int:pk>/",
        views.AdminCategoryDeleteView.as_view(),
        name="admin_category_delete",
    ),
]
