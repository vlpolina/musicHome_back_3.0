from rest_framework import serializers
from shop.models import FavouriteItem, Product

class ProductInFavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'price', 'photo']


class FavouriteItemSerializer(serializers.ModelSerializer):
    product = ProductInFavouriteSerializer()

    class Meta:
        model = FavouriteItem
        fields = ['favourite_item_id', 'product']