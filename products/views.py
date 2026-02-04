from django.db.models import Q, QuerySet
from django.views.generic import DetailView, ListView, TemplateView
from rest_framework import viewsets
from orders.cart import Cart
from .models import Category, Product
from .serializers import ProductSerializer


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(is_active=True)[
            :6
        ]  # 6 активных продуктов для главной
        context["categories"] = Category.objects.all()
        context["current_category"] = None
        context["search_query"] = None
        return context


class ProductListView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products"

    def get_queryset(self) -> QuerySet[Product]:
        queryset = Product.objects.filter(is_active=True).select_related("category")

        query = self.request.GET.get("search")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

        category_slug = self.request.GET.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["current_category"] = self.request.GET.get("category")
        context["search_query"] = self.request.GET.get("search")
        return context


from orders.cart import Cart

class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        product_id = str(self.object.id)

        context["cart_quantity"] = cart.cart.get(product_id, {}).get("quantity", 0)
        return context


class GuidesRecipesView(TemplateView):
    template_name = "guides-recipes.html"


class ProductViewSet(viewsets.ModelViewSet):
    """API эндпоинт для просмотра и поиска товаров."""

    serializer_class = ProductSerializer
    filterset_fields = ["category", "price"]
    search_fields = ["name", "description"]

    def get_queryset(self) -> QuerySet[Product]:
        return Product.objects.filter(is_active=True).select_related("category")
