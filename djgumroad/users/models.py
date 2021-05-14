from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from djgumroad.products.models import Product, PurchasedProduct


class User(AbstractUser):
    """Default user for djgumroad."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)    

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class UserLibrary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)

    class Meta:
        verbose_name_plural = "UserLibraries"

    def __str__(self):
        return self.user.email


def post_save_user_reciever(sender, instance, created, **kwargs):
    if created:
        library = UserLibrary.objects.create(user=instance)

        # assign all the anonymous checkputs / products they purchased
        purchased_products = PurchasedProduct.objects.filter(email=instance.email)
        print(purchased_products)
        for purchased_product in purchased_products:
            library.products.add(purchased_product.product)


post_save.connect(post_save_user_reciever, sender=User)