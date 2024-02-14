from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html

from store.models import Store, Product
from store.models.orders import Order, OrderProduct

user_model = get_user_model()


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
        'admin_link',
        'number_of_managers_link',
    )

    list_filter = (
        'admin',
    )

    search_fields = (
        'name',
        'description',
        'admin__username',
    )

    def admin_link(self, obj):
        link = reverse("admin:auth_user_change", args=(obj.admin.id,))
        return format_html(
            "<a href={}>{}: {}</a>",
            link,
            obj.admin.id,
            obj.admin.username,
        )

    admin_link.short_description = "Admin"

    def number_of_managers_link(self, obj):
        query = "?id__in={}".format(
            ','.join(map(str, obj.managers.values_list('id', flat=True)))
        )
        link = reverse("admin:auth_user_changelist") + query
        return format_html(
            "<a href={}>{}</a>",
            link,
            obj.managers.count(),
        )

    number_of_managers_link.short_description = "Number of managers"


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
