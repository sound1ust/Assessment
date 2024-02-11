from django.db import models

from store.models.stores import Store


class Product(models.Model):
    name = models.CharField(
        verbose_name="Name",
        max_length=50,
        unique=True,
    )
    description = models.TextField(
        verbose_name="Description",
        max_length=256,
    )
    store = models.ForeignKey(
        verbose_name="Store",
        to=Store,
        on_delete=models.PROTECT,
    )
    price = models.FloatField()
    currency = models.CharField(
        verbose_name="Currency",
        max_length=3,
    )

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = "Product"
        verbose_name_plural = "Products"
