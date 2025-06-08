from rest_framework import serializers
from shop.models import Order, OrderItem


class CreateOrderItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    count = serializers.IntegerField(min_value=1)


class CreateOrderSerializer(serializers.Serializer):
    address = serializers.CharField()
    delivery_id = serializers.IntegerField()
    items = CreateOrderItemSerializer(many=True)

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Список товаров не может быть пустым.")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    class Meta:
        model = OrderItem
        fields = ("product", "product_name", "count", "sum_cost")


class OrderDetailSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    delivery_type = serializers.CharField(source="delivery_type.type")

    class Meta:
        model = Order
        fields = ("order_id", "address", "delivery_type", "created_at", "payment_status", "status", "items")

    def get_items(self, obj):
        items = OrderItem.objects.filter(order=obj)
        return OrderItemSerializer(items, many=True).data


class OrderHistorySerializer(serializers.ModelSerializer):
    delivery_type = serializers.CharField(source="delivery_type.type")
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("order_id", "address", "delivery_type", "created_at", "total_cost")

    def get_total_cost(self, obj):
        return sum(item.sum_cost for item in OrderItem.objects.filter(order=obj))
