from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Book, CartItem, Order, OrderItem
from datetime import datetime
import random
import string
from bson.decimal128 import Decimal128
from decimal import Decimal


# ✅ Hàm ép kiểu an toàn cho Decimal / Decimal128 / str / None
def safe_decimal(value):
    if isinstance(value, Decimal128):
        return value.to_decimal()
    elif isinstance(value, Decimal):
        return value
    elif isinstance(value, (int, float, str)):
        try:
            return Decimal(str(value))
        except:
            return Decimal(0)
    return Decimal(0)


def get_session_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def homepage(request):
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')

    all_books = list(Book.objects.all())

    if search:
        all_books = [
            b for b in all_books
            if search.lower() in b.title.lower() or search.lower() in b.author.lower()
        ]

    if category:
        all_books = [b for b in all_books if b.category == category]

    trending_books = [b for b in all_books if getattr(b, "is_trending", False)][:10]
    new_books = sorted(
        [b for b in all_books if getattr(b, "is_new", False)],
        key=lambda x: getattr(x, "created_at", None) or 0,
        reverse=True
    )[:10]

    # ✅ Fix Decimal128 lỗi khi sort rating
    top_rated_books = sorted(
        all_books,
        key=lambda x: float(safe_decimal(x.rating)),
        reverse=True
    )[:10]

    categories = sorted(set(b.category for b in all_books if b.category))

    session_id = get_session_id(request)
    cart_count = CartItem.objects.filter(session_id=session_id).count()

    context = {
        "books": all_books,
        "trending_books": trending_books,
        "new_books": new_books,
        "top_rated_books": top_rated_books,
        "categories": categories,
        "search": search,
        "selected_category": category,
        "cart_count": cart_count,
    }

    return render(request, "books/homepage.html", context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.rental_price_per_day = safe_decimal(book.rental_price_per_day)
    book.rating = safe_decimal(book.rating)

    return render(request, "books/book_detail.html", {"book": book})
def view_all_books(request, filter_type):
    all_books = list(Book.objects.all())

    if filter_type == 'trending':
        books = [b for b in all_books if getattr(b, "is_trending", False)]
        title = "Sách Thịnh Hành"
    elif filter_type == 'new':
        books = sorted(
            [b for b in all_books if getattr(b, "is_new", False)],
            key=lambda x: getattr(x, "created_at", None) or 0,
            reverse=True
        )
        title = "Sách Mới Cập Nhật"
    elif filter_type == 'top_rated':
        books = sorted(
            all_books,
            key=lambda x: float(safe_decimal(x.rating)),
            reverse=True
        )
        title = "Sách Đánh Giá Cao Nhất"
    else:
        books = all_books
        title = "Tất Cả Sách"

    categories = sorted(set(b.category for b in all_books if b.category))
    session_id = get_session_id(request)
    cart_count = CartItem.objects.filter(session_id=session_id).count()

    context = {
        'books': books,
        'title': title,
        'categories': categories,
        'cart_count': cart_count,
    }
    return render(request, 'books/View_All.html', context)


def add_to_cart(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        rental_days = int(request.POST.get('rental_days', 7))
        session_id = get_session_id(request)

        price_per_day = safe_decimal(book.rental_price_per_day)
        cart_item = CartItem.objects.filter(
            session_id=session_id,
            book_id=str(book_id)
        ).first()

        if cart_item:
            cart_item.rental_days = rental_days
            cart_item.price_per_day = price_per_day
            # ✅ Cập nhật hình ảnh nếu có
            if hasattr(book, 'cover_image') and book.cover_image:
                cart_item.book_image = book.cover_image.url if hasattr(book.cover_image, 'url') else str(
                    book.cover_image)
            cart_item.save()
            messages.success(request, f'Đã cập nhật "{book.title}" trong giỏ hàng!')
        else:
            # ✅ Lấy URL hình ảnh
            book_image = ''
            if hasattr(book, 'cover_image') and book.cover_image:
                book_image = book.cover_image.url if hasattr(book.cover_image, 'url') else str(book.cover_image)

            CartItem.objects.create(
                session_id=session_id,
                book_id=str(book_id),
                book_title=book.title,
                book_image=book_image,  # ✅ Thêm hình ảnh
                rental_days=rental_days,
                price_per_day=price_per_day
            )
            messages.success(request, f'Đã thêm "{book.title}" vào giỏ hàng!')

    return redirect('cart')


def cart(request):
    session_id = get_session_id(request)
    cart_items = CartItem.objects.filter(session_id=session_id)

    # ✅ Tính tổng tiền cho từng item
    cart_items_with_subtotal = []
    total = 0

    for item in cart_items:
        price = float(safe_decimal(item.price_per_day))
        subtotal = price * int(item.rental_days)
        total += subtotal

        # Thêm subtotal vào item để hiển thị
        item.subtotal = subtotal
        cart_items_with_subtotal.append(item)

    cart_count = len(cart_items_with_subtotal)

    context = {
        'cart_items': cart_items_with_subtotal,
        'total': total,
        'cart_count': cart_count,
    }
    return render(request, 'books/cart.html', context)


def remove_from_cart(request, item_id):
    session_id = get_session_id(request)
    cart_item = get_object_or_404(CartItem, id=item_id, session_id=session_id)
    cart_item.delete()
    messages.success(request, 'Đã xóa sách khỏi giỏ hàng!')
    return redirect('cart')


def checkout(request):
    session_id = get_session_id(request)
    cart_items = CartItem.objects.filter(session_id=session_id)

    if not cart_items:
        messages.error(request, 'Giỏ hàng trống!')
        return redirect('cart')

    total = sum(
        float(safe_decimal(item.price_per_day)) * int(item.rental_days)
        for item in cart_items
    )
    cart_count = cart_items.count()

    context = {
        'cart_items': cart_items,
        'total': total,
        'cart_count': cart_count,
    }
    return render(request, 'books/checkout.html', context)


def process_order(request):
    if request.method == 'POST':
        session_id = get_session_id(request)
        cart_items = CartItem.objects.filter(session_id=session_id)

        if not cart_items:
            messages.error(request, 'Giỏ hàng trống!')
            return redirect('cart')

        order_number = 'ORD' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

        total = sum(
            float(safe_decimal(item.price_per_day)) * int(item.rental_days)
            for item in cart_items
        )

        order = Order.objects.create(
            order_number=order_number,
            customer_name=request.POST.get('name'),
            customer_email=request.POST.get('email'),
            customer_phone=request.POST.get('phone'),
            customer_address=request.POST.get('address'),
            total_amount=Decimal(str(total)),
            payment_method=request.POST.get('payment_method'),
            status='confirmed'
        )

        for item in cart_items:
            price = safe_decimal(item.price_per_day)
            subtotal = price * Decimal(item.rental_days)

            OrderItem.objects.create(
                order_id=str(order.id),
                book_id=item.book_id,
                book_title=item.book_title,
                rental_days=item.rental_days,
                price_per_day=price,
                subtotal=subtotal
            )

            # Giảm số lượng sách có sẵn
            book = Book.objects.get(id=item.book_id)

            # ✅ Convert all Decimal128 fields to Decimal before saving
            book.rental_price_per_day = safe_decimal(book.rental_price_per_day)
            book.rating = safe_decimal(book.rating)
            # Add any other Decimal128 fields that might exist in your Book model

            book.available_copies = max(0, book.available_copies - 1)
            book.save()

        cart_items.delete()

        messages.success(request, f'Đặt hàng thành công! Mã đơn hàng: {order_number}')
        return redirect('order_success', order_id=order.id)

    return redirect('checkout')


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order_id=str(order_id))

    context = {
        'order': order,
        'order_items': order_items,
        'cart_count': 0,
    }
    return render(request, 'books/order_success.html', context)