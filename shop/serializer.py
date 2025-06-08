from rest_framework import serializers
from .models import *


class ProductCatalogSerializer(serializers.ModelSerializer):
    in_cart = serializers.SerializerMethodField()
    in_favourite = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['product_id', 'slug', 'name', 'short_desc', 'price', 'amount', 'photo', 'category_name', 'brand_name', 'in_cart', 'in_favourite']

    def get_category_name(self, obj):
        return obj.cat.name if obj.cat else None

    def get_brand_name(self, obj):
        return obj.brand_name.name if obj.brand_name else None

    def get_in_cart(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return CartItem.objects.filter(cart__client_id=user, product=obj).exists()
        return None

    def get_in_favourite(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return FavouriteItem.objects.filter(favourite__client_id=user, product=obj).exists()
        return None


class ProductSerializer(serializers.ModelSerializer):
    in_cart = serializers.SerializerMethodField()
    in_favourite = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['product_id', 'slug', 'name', 'long_desc', 'short_desc', 'price', 'amount', 'photo', 'category_name', 'brand_name', 'in_cart', 'in_favourite']

    def get_category_name(self, obj):
        return obj.cat.name if obj.cat else None

    def get_brand_name(self, obj):
        return obj.brand_name.name if obj.brand_name else None

    def get_in_cart(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return CartItem.objects.filter(cart__client_id=user, product=obj).exists()
        return None

    def get_in_favourite(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return FavouriteItem.objects.filter(favourite__client_id=user, product=obj).exists()
        return None


class AdminProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"