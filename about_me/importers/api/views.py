from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from about_me.importers.orders.models import Order, ProductItem
from about_me.importers.api.serializers import OrderSerializer, ProductItemSerializer


class OrderListView(APIView):

	def get(self, request):
		queryset = Order.objects.filter(status='0').order_by('order_number')
		serializer = OrderSerializer(queryset, many=True)
		return Response(serializer.data)


class ProductItemListView(APIView):

	def get(self, request):
		queryset = ProductItem.objects.filter(pk__in=[
            x.pk for x in ProductItem.objects.all()
            if x.order_status() == '0'
   		]).order_by('order_number')
		serializer = ProductItemSerializer(queryset, many=True)
		return Response(serializer.data)


# class PostOrderAPIView(RetrieveAPIView):
# 	queryset = Order.objects.all()
# 	serializer_class = OrderSerializer


# class PostProductItemAPIView(RetrieveAPIView):
# 	queryset = ProductItem.objects.all()
# 	serializer_class = ProductSerializer
