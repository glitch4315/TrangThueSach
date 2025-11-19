from djongo import models
from django.utils import timezone

from decimal import Decimal
from djongo import models
from bson import ObjectId

class Book(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    description = models.TextField()
    cover_image = models.CharField(max_length=500)
    category = models.CharField(max_length=50)
    publication_year = models.IntegerField()
    rental_price_per_day = models.FloatField()
    available_copies = models.IntegerField()
    total_copies = models.IntegerField()
    rating = models.FloatField()
    is_trending = models.BooleanField()
    is_new = models.BooleanField()
    views = models.IntegerField()

    @property
    def id(self):
        return str(self._id)

    class Meta:
        db_table = 'books'

    def __str__(self):
        return self.title


class CartItem(models.Model):
    session_id = models.CharField(max_length=40)
    book_id = models.ObjectIdField()
    book_title = models.CharField(max_length=255)
    book_image = models.ImageField(upload_to='cart/', blank=True, null=True)
    rental_days = models.IntegerField(default=7)
    price_per_day = models.FloatField(default=0.0)
    added_at = models.DateTimeField(default=timezone.now)

    def total_price(self):
        return self.rental_days * self.price_per_day

    def __str__(self):
        return f"{self.book_title} ({self.rental_days} days)"


class Order(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    order_number = models.CharField(max_length=12, unique=True)
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    customer_address = models.TextField()
    total_amount = models.FloatField(default=0.0)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book_id = models.ObjectIdField()
    book_title = models.CharField(max_length=200)
    rental_days = models.IntegerField()
    price_per_day = models.FloatField()
    subtotal = models.FloatField()

    class Meta:
        db_table = 'order_items'

class Rental(models.Model):
    order_id = models.CharField(max_length=100)
    order_number = models.CharField(max_length=50)
    book_id = models.CharField(max_length=100)
    book_title = models.CharField(max_length=200)
    book_cover = models.URLField(blank=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    rental_days = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)

    rental_date = models.DateTimeField(auto_now_add=True)
    expected_return_date = models.DateTimeField()
    actual_return_date = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=20, default='active')
    late_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rentals'

    def __str__(self):
        return f"{self.book_title} - {self.customer_name}"

    def is_overdue(self):
        """Kiểm tra xem đã quá hạn chưa"""
        if self.status == 'returned':
            return False
        return timezone.now() > self.expected_return_date

    def days_overdue(self):
        """Số ngày quá hạn"""
        if not self.is_overdue():
            return 0
        delta = timezone.now() - self.expected_return_date
        return delta.days

    def calculate_late_fee(self):
        """Tính phí trễ hạn (10k/ngày)"""
        if self.is_overdue() and self.status != 'returned':
            return self.days_overdue() * 10
        return 0