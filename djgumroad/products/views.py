from django.views import generic
from .models import Product


class ProductListView(generic.ListView):
    template_name = "discover.html"
    queryset = Product.objects.all()