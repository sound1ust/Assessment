from django.contrib import admin
from django.conf.global_settings import AUTH_USER_MODEL

from store.models import Store, Product
from store.models.orders import Order, OrderProduct

user_model = AUTH_USER_MODEL


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'store',
        'customer',
    )

    list_filter = (
        'created_at',
        'store',
        'customer',
    )

    search_fields = (
        'created_at',
        'store__name',
        'customer__username',
    )

    fields = (
        'store',
        'customer',
    )

    inlines = [
        OrderProductInline,
    ]


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'product',
        'quantity',
    )

    list_filter = (
        'order',
        'product',
        'quantity',
    )

    search_fields = (
        'order__id',
        'product__name',
        'quantity',
    )


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'admin',
        'display_managers',
    )

    list_filter = (
        'name',
        'description',
        'admin',
    )

    search_fields = (
        'name',
        'description',
        'admin__username',
    )

    def display_managers(self, obj):
        return ", ".join([manager.username for manager in obj.managers.all()])

    display_managers.short_description = 'Managers'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'store',
        'price',
        'currency',
    )

    list_filter = (
        'name',
        'description',
        'store',
        'price',
        'currency',
    )

    search_fields = (
        'name',
        'description',
        'store__name',
        'price',
        'currency',
    )
