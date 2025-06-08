from django.db import models
from django.urls import reverse


class Category(models.Model):
    category_id = models.AutoField("ID", primary_key=True)
    name = models.TextField(db_index=True, verbose_name="Название")
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'
        ordering = ['name']


class Brand(models.Model):
    brand_id = models.AutoField("ID", primary_key=True)
    name = models.TextField(db_index=True, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('brand', kwargs={'brand_id': self.pk})

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['name']


class Delivery(models.Model):
    delivery_id = models.AutoField("ID", primary_key=True)
    type = models.TextField(db_index=True, verbose_name="Тип доставки")
    delivery_time = models.IntegerField(verbose_name="Время доставки (ч)")
    cost = models.IntegerField(verbose_name="Стоимость доставки (руб)")
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse('delivery', kwargs={'delivery_id': self.pk})

    class Meta:
        verbose_name = 'Вариант доставки'
        verbose_name_plural = 'Варианты доставки'
        ordering = ['type']


class Product(models.Model):
    product_id = models.AutoField("ID", primary_key=True)
    name = models.TextField(verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория")
    short_desc = models.TextField(verbose_name="Короткое описание")
    long_desc = models.TextField(verbose_name="Длинное описание")
    price = models.FloatField(verbose_name="Цена")
    amount = models.IntegerField(verbose_name="Количество на складе")
    brand_name = models.ForeignKey('Brand', on_delete=models.PROTECT, verbose_name="Бренд")
    photo = models.ImageField(upload_to="photos/", verbose_name="Фото")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_id': self.pk})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['updated_at', 'name']


class Order(models.Model):
    order_id = models.AutoField("ID", primary_key=True)
    client_id = models.ForeignKey('auth.User', on_delete=models.PROTECT, verbose_name="ID клиента")
    cart_id = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name="ID корзины")
    address = models.TextField(default='', verbose_name="Адрес доставки")
    payment_status = models.BooleanField(default=False, verbose_name="Статус оплаты")
    status = models.BooleanField(default=False, verbose_name="Статус доставки")
    delivery_type = models.ForeignKey('Delivery', on_delete=models.PROTECT, verbose_name="Тип доставки")
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name="Дата оформления")

    def get_absolute_url(self):
        return reverse('order', kwargs={'order_id': self.pk})

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['created_at']


class OrderItem(models.Model):
    order_item_id = models.AutoField("ID", primary_key=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name="ID заказа")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name="ID товара")
    count = models.IntegerField(verbose_name="Количество")
    sum_cost = models.FloatField(verbose_name="Стоимость")
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name="Дата создания")

    def get_absolute_url(self):
        return reverse('orderItem', kwargs={'order_item_id': self.pk})

    class Meta:
        verbose_name = 'Товар из заказа'
        verbose_name_plural = 'Товары из заказа'
        ordering = ['created_at']


class Cart(models.Model):
    cart_id = models.AutoField("ID", primary_key=True)
    client_id = models.ForeignKey('auth.User', on_delete=models.PROTECT, verbose_name="ID клиента")
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name="Дата обновления")

    def get_absolute_url(self):
        return reverse('cart', kwargs={'cart_id': self.pk})

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        ordering = ['updated_at']


class CartItem(models.Model):
    cart_item_id = models.AutoField("ID", primary_key=True)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name="ID корзины")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name="ID товара")
    count = models.IntegerField(verbose_name="Количество")
    sum_cost = models.FloatField(verbose_name="Стоимость")
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name="Дата обновления")

    def get_absolute_url(self):
        return reverse('cartItem', kwargs={'cart_item_id': self.pk})

    class Meta:
        verbose_name = 'Товар из корзины'
        verbose_name_plural = 'Товары из корзины'
        ordering = ['updated_at']


class Favourite(models.Model):
    favourite_id = models.AutoField("ID", primary_key=True)
    client_id = models.ForeignKey('auth.User', on_delete=models.PROTECT, verbose_name="ID клиента")
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name="Дата создания")

    def get_absolute_url(self):
        return reverse('favourite', kwargs={'favourite_id': self.pk})

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ['created_at']


class FavouriteItem(models.Model):
    favourite_item_id = models.AutoField("ID", primary_key=True)
    favourite = models.ForeignKey('Favourite', on_delete=models.CASCADE, verbose_name="ID корзины")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name="ID товара")
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name="Дата создания")

    def get_absolute_url(self):
        return reverse('favouriteItem', kwargs={'favourite_item_id': self.pk})

    class Meta:
        verbose_name = 'Товар из избранного'
        verbose_name_plural = 'Товары из избранного'
        ordering = ['created_at']


class Feedback(models.Model):
    feedback_id = models.AutoField("ID", primary_key=True)
    creator_id = models.ForeignKey('auth.User', on_delete=models.PROTECT, verbose_name="ID клиента")
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name="ID товара")
    feedback = models.TextField(verbose_name="Текст отзыва")
    answer = models.TextField(verbose_name="Ответ на отзыв")
    is_blocked = models.BooleanField(default=False, verbose_name="Блокировка")
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name="Дата обновления")

    def get_absolute_url(self):
        return reverse('feedback', kwargs={'feedback_id': self.pk})

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['updated_at']