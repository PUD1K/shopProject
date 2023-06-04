from django.shortcuts import render
from collections import defaultdict
import json
import pprint

from rest_framework.decorators import api_view,  authentication_classes, permission_classes
from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from .models import Order, OrderItem
from .serializers import OrderItemSerializer, OrderSerializer, MyOrderSerializer

# Create your views here.

@api_view(['POST'])

@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
# создание заказа
def checkout(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])
        serializer.save(user=request.user, paid_amount=paid_amount)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # request.user - получаем из headers.токена
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)
    
class AllOrders(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # request.user - получаем из headers.токена
        orders = Order.objects.all()
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)

class AllOrderList(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # request.user - получаем из headers.токена
        orders = Order.objects.all()
        serializer = MyOrderSerializer(orders, many=True)
        statsSalesPerMonth = defaultdict(int)
        statsSalesPerCategory = defaultdict(int)
        statsTotalSumPerMonth = defaultdict(int)

        for order in serializer.data:
            month = getRusMonth(order['created_at'][5:7])
            for item in order['items']:
                product = item['product']
                statsSalesPerMonth[month] += item['quantity']
                print(item)
                print(int(item['price'][:-3]))
                print(item['quantity'])
                statsTotalSumPerMonth[month] += (int(item['price'][:-3]) * item['quantity'])/1000
                statsSalesPerCategory[product['category']] += item['quantity']
        
        return Response({
            'statsSalesPerMonth': statsSalesPerMonth, 
            'statsPricePerMonth': statsTotalSumPerMonth, 
            'statsSalesPerCategory': statsSalesPerCategory
        })


def getRusMonth(month): 
    months = {
        "01": "Январь",
        "02": "Февраль",
        "03": "Март",
        "04": "Апрель",
        "05": "Май",
        "06": "Июнь",
        "07": "Июль",
        "08": "Август",
        "09": "Сентябрь",
        "10": "Октябрь",
        "11": "Ноябрь",
        "12": "Декабрь",
    }

    return months[month] if months[month] != None else ''

@api_view(['POST'])
def getAllOrdersByNumber(request):
    number = request.data.get('number')
    print(number)
    if(number is None or number == ''):
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(pk=number)
    orders_serializer = MyOrderSerializer(orders, many=True)
    return Response(orders_serializer.data)

@api_view(['POST'])
def changeOrderStatus(request):
    status = request.data.get('status')
    number = request.data.get('number')
    print(status)
    print(number)

    order = Order.objects.get(pk=number)
    order.status = status;
    order.save()
    order_serializer = MyOrderSerializer(order)
    return Response(order_serializer.data)