from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import uuid


def pin():
    return uuid.uuid4().hex[:6].upper()

class Client(models.Model):
    client = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    primary_email = models.EmailField(max_length=100)
    secondary_email = models.EmailField(max_length=100, blank=True)
    primary_mobile = models.CharField(max_length=20, null=True)
    secondary_mobile = models.CharField(max_length=20, null=True, blank=True)
    unique_pin = models.CharField(max_length=6, default=pin, editable=False, unique=True)

    class Meta:
        ordering = ["client"]

    def __str__(self):
        return self.client


class Order(models.Model):
    STATUS_CHOICES = (
        ('', 'Packing'),
        ('0', 'Awaiting Delivery'),
        ('1', 'In Transit'),
        ('2', 'Delivered')
    )
    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100, verbose_name="Order No.")
    due = models.DateTimeField(default=datetime.now()+timedelta(hours=24))
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, blank=True)
    discount = models.DecimalField(blank=True, default=0, null=True, max_digits=8, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    delivered_by = models.CharField(max_length=100, editable=False, default="-")
    old_status = models.CharField(max_length=100, editable=False, null=True)

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        self.old_status = self.status

    def __str__(self):
        return str(self.order_number)

    def address(self):
        return self.client.address

    def products(self):
        return ProductItem.objects.filter(order_number=self)

    def total_price(self):
        subtotal = 0
        for product in self.products():
            subtotal = subtotal + (product.price()*int(product.quantity))
        if self.discount > 0:
            total = (subtotal - self.discount)
        else:
            total = subtotal
        return u"R {}".format(total)

    def client_name(self):
        return self.client.client

    #def save(self):
    #    if self.old_status == '0' and self.status == '1':
    #        super(Order, self).save()


class Product(models.Model):
    PRODUCT_CHOICES = (
        ('', '- Select -'),
        ('(Bn)', 'Beans'),
        ('(Flt)', 'Filter'),
        ('(C)', 'Capsules'),
        ('(CM)', 'Coffee Machine'),
        ('(IC)', 'Instant Coffees'),
        ('(T)', 'Teas'),
        ('(IHB)', 'Instant Hot Beverages'),
        ('(S)', 'Smoothies'),
        ('(Con)', 'Consumables'),
        ('(C&L)', 'Take away cups and lids'),
        ('(CMC)', 'Coffee Machine Consumables')
    )
    description = models.CharField(max_length=100, verbose_name="Description", choices=PRODUCT_CHOICES)
    name = models.CharField(max_length=100, verbose_name="Name")
    volume = models.CharField(max_length=100, verbose_name="Volume")
    product_code = models.CharField(max_length=5, verbose_name="Code")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        ordering = ("description", "name", "volume", "product_code")

    def __str__(self):
        return u"{} - {} - {} - {}".format(
            self.description,
            self.name,
            self.volume,
            self.product_code
        )


class ProductItem(models.Model):
    order_number = models.ForeignKey("Order", null=True)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)

    def order_id(self):
        return self.order_number_id

    def order_status(self):
        return self.order_number.status

    def product_description(self):
        return self.product.get_description_display()

    def product_name(self):
        return self.product.name

    def product_volume(self):
        return self.product.volume

    def product_code(self):
        return self.product.product_code

    def price(self):
        return self.product.price


class Department(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    warehouse = models.BooleanField(default=False)
    driver = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


import signals