from django.shortcuts import render

from rest_framework.decorators import api_view,  authentication_classes, permission_classes
from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .serializers import OrderSerializer, MyOrderSerializer

# Create your views here.

@api_view(['POST'])

@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
# создание заказа
def checkout(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])

        try:
            serializer.save(user=request.user, paid_amount=paid_amount)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
