"""Views for the products app."""

from typing import TYPE_CHECKING, Any

from django.db.models import Avg, Count, FloatField, Q, QuerySet
from django.db.models.functions import Coalesce
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from rest_framework import viewsets

from orders.cart import Cart
from reviews.forms import ReviewForm

from .models import Category, Product
from .serializers import ProductSerializer

if TYPE_CHECKING:
    ProductList = ListView[Product]
    ProductModel = viewsets.ModelViewSet[Product]
    ProductDetail = DetailView[Product]
else:
    ProductList = ListView
    ProductModel = viewsets.ModelViewSet
    ProductDetail = DetailView


class HomeView(TemplateView):
    """Home page view."""

    template_name = "home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get context data."""
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(is_active=True)[
            :6
        ]  # 6 активных продуктов для главной
        context["categories"] = Category.objects.all()
        context["current_category"] = None
        context["search_query"] = None
        return context


class ProductListView(ProductList):
    """Product list view."""

    model = Product
    template_name = "home.html"
    context_object_name = "products"
    paginate_by = 9  # 👈 ВАЖНО

    def get_queryset(self) -> QuerySet[Product]:
        """Get queryset."""
        queryset = (
            Product.objects.filter(is_active=True)
            .select_related("category")
            .annotate(
                avg_rating=Coalesce(
                    Avg("reviews__rating"), 0.0, output_field=FloatField()
                ),
                reviews_count=Count("reviews"),
            )
        )

        # 🔍 поиск
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        # 🗂 категория
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category__slug=category)

        # 🔃 сортировка
        sort = self.request.GET.get("sort", "price")
        if sort == "price":
            queryset = queryset.order_by("price")
        elif sort == "name":
            queryset = queryset.order_by("name")
        elif sort == "popular":
            queryset = queryset.order_by("-avg_rating", "-reviews_count")

        return queryset

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Get request."""
        response = super().get(request, *args, **kwargs)

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return render(request, "home.html", self.get_context_data())

        return response

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get context data."""
        context = super().get_context_data(**kwargs)

        querydict = self.request.GET.copy()
        querydict.pop("page", None)
        querydict.pop("sort", None)

        context["querystring"] = querydict.urlencode()

        context["categories"] = Category.objects.all()
        context["current_category"] = self.request.GET.get("category")
        context["search_query"] = self.request.GET.get("search")
        context["current_sort"] = self.request.GET.get("sort", "price")
        return context


class ProductDetailView(ProductDetail):
    """Product detail view."""

    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get context data."""
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        product_id = str(self.object.id)

        context["cart_quantity"] = cart.cart.get(product_id, {}).get("quantity", 0)

        reviews_qs = self.object.reviews.select_related("user").order_by("-created_at")
        context["reviews"] = reviews_qs

        user = self.request.user
        has_reviewed = False

        if user.is_authenticated:
            has_reviewed = reviews_qs.filter(user=user).exists()

        context["has_reviewed"] = has_reviewed
        context["review_form"] = ReviewForm()

        return context


class GuidesRecipesView(TemplateView):
    """Guides and recipes view."""

    template_name = "guides-recipes.html"


class ProductViewSet(ProductModel):
    """API эндпоинт для просмотра и поиска товаров."""

    serializer_class = ProductSerializer
    filterset_fields = ["category", "price"]
    search_fields = ["name", "description"]

    def get_queryset(self) -> QuerySet[Product]:
        """Get queryset."""
        return Product.objects.filter(is_active=True).select_related("category")
