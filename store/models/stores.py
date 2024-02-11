from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models

user_model = AUTH_USER_MODEL


class Store(models.Model):
    name = models.CharField(
        verbose_name="Name",
        max_length=50,
        unique=True,
    )
    description = models.TextField(
        verbose_name="Description",
        max_length=256,
    )
    admin = models.ForeignKey(
        verbose_name="Admin",
        to=user_model,
        on_delete=models.PROTECT,
    )
    managers = models.ManyToManyField(
        verbose_name="Managers",
        to=user_model,
        blank=True,
        related_name="store_managers",
    )

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = "Store"
        verbose_name_plural = "Stores"
