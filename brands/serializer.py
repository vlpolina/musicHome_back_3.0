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