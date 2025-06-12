from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from shop.models import Product, Order, OrderItem, Category, Brand, Cart, Delivery

User = get_user_model()


def create_user(username='testuser', password='testpass123'):
    user = User.objects.create_user(username=username, password=password)
    return user


def create_product(name='Test Product'):
    return Product.objects.create(
        name=name,
        slug='test-product',
        cat_id=1,
        short_desc='short',
        long_desc='long',
        price=100.0,
        amount=10,
        brand_name_id=1,
        photo='photos/test.jpg',
        is_published=True,
    )


class AddFeedbackTests(APITestCase):
    def setUp(self):
        self.url = reverse('feedbacks:add')
        self.user = create_user()
        self.user2 = create_user('otheruser', 'otherpass123')

        category = Category.objects.create(name="Category1")
        brand = Brand.objects.create(name="Brand1", description="Desc")
        delivery = Delivery.objects.create(type='Доставка курьером', cost=300, delivery_time=3)

        self.product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            cat=category,
            short_desc="short",
            long_desc="long",
            price=100.0,
            amount=10,
            brand_name=brand,
            photo="photos/test.jpg",
            is_published=True,
        )

        self.cart = Cart.objects.create(client_id=self.user)

        self.completed_order = Order.objects.create(
            client_id=self.user,
            cart_id=self.cart,
            address='Tomsk',
            payment_status=True,
            status=True,
            delivery_type=delivery,
        )

        OrderItem.objects.create(
            order=self.completed_order,
            product=self.product,
            count=1,
            sum_cost=100,
        )

        self.other_order = Order.objects.create(
            client_id=self.user2,
            cart_id=self.cart,
            address="Other address",
            payment_status=True,
            status=True,
            delivery_type_id=delivery.delivery_id,
        )

    def test_add_feedback_success(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "product_id": self.product.product_id,
            "feedback": "Отличный товар!"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['feedback'], data['feedback'])
        self.assertEqual(response.data['creator_id'], self.user.id)

    def test_add_feedback_unauthenticated(self):
        data = {"product_id": self.product.product_id, "feedback": "Test"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_feedback_missing_product_id(self):
        self.client.force_authenticate(user=self.user)
        data = {"feedback": "Test"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("product_id обязателен", response.data['error'])

    def test_add_feedback_missing_feedback(self):
        self.client.force_authenticate(user=self.user)
        data = {"product_id": self.product.product_id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("feedback обязателен", response.data['error'])

    def test_add_feedback_product_not_found(self):
        self.client.force_authenticate(user=self.user)
        data = {"product_id": 9999999, "feedback": "Test"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Продукт не найден", response.data['error'])

    def test_add_feedback_user_not_ordered_product(self):
        self.client.force_authenticate(user=self.user2)  # пользователь без заказа с этим продуктом
        data = {"product_id": self.product.product_id, "feedback": "Test"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("Вы не можете оставить отзыв на этот товар", response.data['error'])
