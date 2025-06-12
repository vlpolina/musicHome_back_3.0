from rest_framework import serializers
from shop.models import Delivery


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['delivery_id', 'type', 'delivery_time', 'cost']


class AdminDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = "__all__"


class DeliveryStatsSerializer(serializers.Serializer):
    delivery_id = serializers.IntegerField()
    type = serializers.CharField()
    total_orders = serializers.IntegerField()
    avg_time = serializers.FloatField()
    total_revenue = serializers.FloatField(allow_null=True)