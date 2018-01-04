from django.contrib import admin
from about_me.importers.orders.models import Order, Product, Client, ProductItem


class ProductItemInline(admin.TabularInline):
    model = ProductItem
    fields = ["product", "quantity"]
    extra = 1
    can_delete = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "order_number",
        "total_price",
        "created",
        "due",
        "updated",
        "status",
        "delivered_by"
    )
    list_filter = ("client", "order_number", "due", "status")
    can_delete = True

    inlines = [
        ProductItemInline,
    ]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("client", "address", "primary_email", "primary_mobile", "unique_pin")


@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ("description", "name", "volume", "product_code", "price")
