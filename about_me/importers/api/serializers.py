from rest_framework import serializers
from about_me.importers.orders.models import Order, ProductItem


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
        	"client",
        	"id",
        	"order_number",
        	"client_name",
        	"address",
        )

class ProductItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductItem
        fields = (
        	"order_id",
            "order_number",
        	"product",
        	"product_name",
        	"product_volume",
        	"code",
        	"price",
        )