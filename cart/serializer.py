from rest_framework import serializers
from shop.models import CartItem, Product

class ProductInCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'price', 'photo']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductInCartSerializer()

    class Meta:
        model = CartItem
        fields = ['cart_item_id', 'product', 'count', 'sum_cost']