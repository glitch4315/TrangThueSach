from djongo import models
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField()
    cover_image = models.URLField(blank=True)
    category = models.CharField(max_length=50)
    publication_year = models.IntegerField()
    rental_price_per_day = models.DecimalField(max_digits=6, decimal_places=2)
    available_copies = models.IntegerField(default=1)
    total_copies = models.IntegerField(default=1)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    is_trending = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'books'

    def __str__(self):
        return self.title


class CartItem(models.Model):
    session_id = models.CharField(max_length=100)
    book_id = models.CharField(max_length=100)
    book_title = models.CharField(max_length=200)
    book_image = models.CharField(max_length=500, blank=True, null=True)
    rental_days = models.IntegerField(default=7)
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart_items'


class Order(models.Model):
    order_number = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    customer_address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'


class OrderItem(models.Model):
    order_id = models.CharField(max_length=100)
    book_id = models.CharField(max_length=100)
    book_title = models.CharField(max_length=200)
    rental_days = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'order_items'