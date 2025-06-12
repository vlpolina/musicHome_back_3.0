from rest_framework import serializers
from shop.models import Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['brand_id', 'name']


class AdminBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class BrandStatsSerializer(serializers.Serializer):
    brand_id = serializers.IntegerField()
    name = serializers.CharField()
    total_products = serializers.IntegerField()
    categories = serializers.ListField(child=serializers.CharField())
    average_price = serializers.FloatField()

