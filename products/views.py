from typing import Any, Self, TYPE_CHECKING

from django.views.generic import DetailView, ListView, TemplateView

from .models import Category, Product

if TYPE_CHECKING:
    ViewList = ListView[Product]
    ViewDetail = DetailView[Product]
else:
    ViewList = ListView
    ViewDetail = DetailView


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self: Self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["features_products"] = Product.objects.filter(is_active=True)[:5]
        return context


class ProductListView(ViewList):
    model = Product
    template_name = "products.html"
    context_object_name = "products"
    queryset = Product.objects.filter(is_active=True)

    def get_context_data(self: Self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ProductDetailView(TemplateView):
    model = Product
    # template_name = "products.html"
    template_name = "product-citra-hops.html"
    slug_field = "slug"
    context_object_name = "product"

    def get_template_names(self):
        # return [f"product-{self.object.slug}.html"]
        return "product-citra-hops.html"


class GuidesRecipesView(TemplateView):
    template_name = "guides-recipes.html"
