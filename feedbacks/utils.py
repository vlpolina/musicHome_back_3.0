from shop.models import OrderItem, Order

def user_ordered_product(user, product):
    return OrderItem.objects.filter(
        order__client_id=user,
        order__status=True,
        order__payment_status=True,
        product=product
    ).exists()
