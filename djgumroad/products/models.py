from django.db import models
from django.urls import reverse


class Product(models.Model):
    user = models.ForeignKey(
        "users.User", 
        on_delete=models.CASCADE, 
        related_name="products"
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    cover = models.ImageField(blank=True, null=True, upload_to="product_covers/")
    slug = models.SlugField()

    # content
    content_url = models.URLField(blank=True, null=True)
    content_file = models.FileField(blank=True, null=True)

    active = models.BooleanField(default=False)
    price = models.PositiveIntegerField(default=1)  # cents

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:product-detail", kwargs={
            "slug": self.slug
        })
    
    def get_update_url(self):
        return reverse('products:product-update', kwargs={
            "slug": self.slug
        })

    def get_delete_url(self):
        return reverse('products:product-delete', kwargs={
            "slug": self.slug
        })

    def price_display(self):
        return "{0:.2f}".format(self.price / 100)


class PurchasedProduct(models.Model):
    email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_purchased = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email