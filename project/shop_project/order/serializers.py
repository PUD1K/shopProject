from rest_framework import serializers

from .models import Order, OrderItem

from product.serializers import ProductSerializer
from product.models import Product

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
            'items',
            'status'
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
            'items',
            'status'
        )
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
            # обновление продаж для каждого товара
            self.update_sales_product(item_data['product'], item_data['quantity'])

        return order

    def update_sales_product(self, name, quantity):
        old_quantity = Product.objects.filter(name=name).values('sales')
        new_quantity = old_quantity[0]['sales'] + quantity
        data = Product.objects.filter(name=name).update(sales = new_quantity)
