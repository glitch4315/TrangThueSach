from django.contrib import admin
from .models import Book, CartItem, Order, OrderItem, Rental


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'rental_price_per_day', 'available_copies', 'rating', 'is_trending', 'is_new']
    list_filter = ['category', 'is_trending', 'is_new']
    search_fields = ['title', 'author', 'isbn']
    list_editable = ['is_trending', 'is_new']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['book_title', 'session_id', 'rental_days', 'added_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'customer_name', 'customer_email']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['book_title', 'order_id', 'rental_days', 'subtotal']


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['book_title', 'customer_name', 'rental_date', 'expected_return_date', 'status', 'is_overdue']
    list_filter = ['status', 'rental_date']
    search_fields = ['book_title', 'customer_name', 'customer_email', 'order_number']
    readonly_fields = ['rental_date', 'created_at', 'updated_at']

    def is_overdue(self, obj):
        return '⚠️ Có' if obj.is_overdue() else '✅ Không'

    is_overdue.short_description = 'Quá hạn'