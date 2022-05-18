from rest_framework import serializers

from .models import Order, OrderItem

from product.serializers import ProductSerializer

# для своих заказов
class MyOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = (
            "price",
            "product",
            "quantity"
        )

# для своих просмотра своих заказов
class MyOrderSerializer(serializers.ModelSerializer):
    # вложенный список
    items = MyOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "phone",
            "created_at",
            "paid_amount",
            'items'
        )


# объект заказа
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "price",
            "product",
            "quantity"
        )

# заказ
class OrderSerializer(serializers.ModelSerializer):
    # вложенный список
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "phone",
            "created_at",
            'items'
        )
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order
