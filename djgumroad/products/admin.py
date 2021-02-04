from django.contrib import admin

from .models import Product, PurchasedProduct


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


admin.site.register(Product, ProductAdmin)
admin.site.register(PurchasedProduct)
