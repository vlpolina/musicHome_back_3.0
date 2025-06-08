from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'name', 'created_at', 'updated_at')
    list_display_links = ('category_id', 'name')
    search_fields = ('name', )
    list_filter = ('created_at', 'updated_at')


class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_id', 'name', 'created_at', 'updated_at')
    list_display_links = ('brand_id', 'name')
    search_fields = ('name', )
    list_filter = ('created_at', 'updated_at')


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('delivery_id', 'type', 'delivery_time', 'cost', 'updated_at')
    list_display_links = ('delivery_id', 'type')
    search_fields = ('type', )
    list_filter = ('delivery_time', 'cost', 'updated_at')


class ProdAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'amount', 'price', 'is_published', 'updated_at')
    list_display_links = ('product_id', 'name')
    search_fields = ('name', 'short_desc')
    list_editable = ('is_published', )
    list_filter = ('amount', 'price', 'is_published', 'updated_at')
    prepopulated_fields = {"slug": ("name",)}


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'client_id', 'cart_id', 'payment_status', 'status', 'created_at')
    list_display_links = ('order_id', 'client_id', 'cart_id')
    search_fields = ('order_id', )
    list_editable = ('payment_status', 'status')
    list_filter = ('payment_status', 'status', 'created_at')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_item_id', 'order', 'product', 'count', 'sum_cost', 'created_at')
    list_display_links = ('order_item_id', 'order', 'product')
    search_fields = ('order_item_id', 'order')
    list_filter = ('created_at', )


class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'client_id', 'created_at', 'updated_at')
    list_display_links = ('cart_id', 'client_id')
    search_fields = ('cart_id', )
    list_filter = ('created_at', 'updated_at')


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart_item_id', 'cart', 'product', 'count', 'sum_cost', 'updated_at')
    list_display_links = ('cart_item_id', 'cart', 'product')
    search_fields = ('cart_item_id', 'cart')
    list_filter = ('created_at', 'updated_at')


class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('favourite_id', 'client_id', 'created_at')
    list_display_links = ('favourite_id', 'client_id')
    search_fields = ('favourite_id', )
    list_filter = ('created_at', )


class FavouriteItemAdmin(admin.ModelAdmin):
    list_display = ('favourite_item_id', 'favourite', 'product', 'created_at')
    list_display_links = ('favourite_item_id', 'favourite', 'product')
    search_fields = ('favourite_item_id', 'favourite')
    list_filter = ('created_at', )


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_id', 'creator_id', 'product_id', 'is_blocked', 'updated_at')
    list_display_links = ('feedback_id', 'creator_id', 'product_id')
    search_fields = ('feedback_id', )
    list_editable = ('is_blocked', )
    list_filter = ('is_blocked', 'created_at', 'updated_at')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(Product, ProdAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Favourite, FavouriteAdmin)
admin.site.register(FavouriteItem, FavouriteItemAdmin)
admin.site.register(Feedback, FeedbackAdmin)
