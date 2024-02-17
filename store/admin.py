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
        'store',
        'customer',
    )

    search_fields = (
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
    )

    search_fields = (
        'product__name',
    )


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'admin_link',
        'number_of_managers_link',
        'number_of_products_link',
    )

    list_filter = (
        'admin',
    )

    search_fields = (
        'name',
        'description',
        'admin__username',
    )

    def get_queryset(self, request):
        self.current_user = request.user
        return super().get_queryset(request)

    def admin_link(self, obj):
        # TODO or create custom perm?
        if not self.current_user.has_perm("auth.view_user"):
            return f"{obj.admin.id}: {obj.admin.username}"

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
        count = obj.managers.count()

        if not self.current_user.has_perm("store.view_store_products"):
            return f"{count}"

        link = reverse("admin:auth_user_changelist") + query
        return format_html(
            "<a href={}>{}</a>",
            link,
            count,
        )

    number_of_managers_link.short_description = "Number of managers"

    def number_of_products_link(self, obj):
        query = f"?store__id__exact={obj.id}"
        # no need for select_related
        count = Product.objects.filter(store__id=obj.id).count()

        if not self.current_user.has_perm("store.view_store_products"):
            return f"{count}"

        link = reverse("admin:store_product_changelist") + query
        return format_html("<a href={}>{}</a>", link, count)

    number_of_products_link.short_description = "Number of products"


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
        'store',
        'currency',
    )

    search_fields = (
        'name',
        'description',
    )
