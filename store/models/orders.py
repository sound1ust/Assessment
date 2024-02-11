from datetime import datetime
from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models

from store.models.products import Product
from store.models.stores import Store

user_model = AUTH_USER_MODEL


class Order(models.Model):
    created_at = models.DateTimeField(
        verbose_name="Created at",
        auto_now_add=True,
        editable=False,
    )
    store = models.ForeignKey(
        verbose_name="Store",
        to=Store,
        on_delete=models.PROTECT,
    )
    customer = models.ForeignKey(
        verbose_name="Customer",
        to=user_model,
        on_delete=models.PROTECT,
    )
    products = models.ManyToManyField(
        verbose_name="Products",
        to=Product,
        through="OrderProduct",
    )

    def __str__(self):
        created_at = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return f"Order of {created_at} by {self.customer} in {self.store}"


class OrderProduct(models.Model):
    order = models.ForeignKey(
        verbose_name="Order",
        to=Order,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        verbose_name="Product",
        to=Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Quantity",
    )

    def __str__(self):
        return f"{self.product} in {self.order}"

    class Meta:
        unique_together = ('order', 'product')
        verbose_name = "Order product"
        verbose_name_plural = "Order products"
