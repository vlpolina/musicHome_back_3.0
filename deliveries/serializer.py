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