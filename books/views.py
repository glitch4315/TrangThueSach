from bson import ObjectId
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
import random
from datetime import datetime, timedelta
import string
import uuid
from .models import Book, CartItem, Order, OrderItem, Rental
from pymongo import MongoClient

mongo_client = MongoClient('localhost', 27017)
mongo_db = mongo_client['bookrental_db']

def safe_decimal(value):
    if isinstance(value, Decimal):
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


# -------------------- HOMEPAGE --------------------
def homepage(request):
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')

    all_books = list(Book.objects.all())

    if search:
        all_books = [b for b in all_books if search.lower() in b.title.lower() or search.lower() in b.author.lower()]

    if category:
        all_books = [b for b in all_books if b.category == category]

    trending_books = [b for b in all_books if getattr(b, "is_trending", False)][:10]
    new_books = sorted(
        [b for b in all_books if getattr(b, "is_new", False)],
        key=lambda x: getattr(x, "created_at", None) or 0,
        reverse=True
    )[:10]

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


# -------------------- BOOK DETAIL --------------------
def book_detail(request, book_id):
    try:
        obj_id = ObjectId(book_id)
    except:
        messages.error(request, "Sách không tồn tại!")
        return redirect('homepage')

    book = get_object_or_404(Book, _id=obj_id)
    return render(request, "books/book_detail.html", {"book": book})


# -------------------- VIEW ALL BOOKS --------------------
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
        books = sorted(all_books, key=lambda x: float(safe_decimal(x.rating)), reverse=True)
        title = "Sách Đánh Giá Cao Nhất"
    else:
        books = all_books
        title = "Tất Cả Sách"

    categories = sorted(set(b.category for b in all_books if b.category))
    session_id = get_session_id(request)
    cart_count = CartItem.objects.filter(session_id=session_id).count()

    context = {
        "books": books,
        "title": title,
        "categories": categories,
        "cart_count": cart_count,
    }
    return render(request, "books/View_All.html", context)

def add_to_cart(request, book_id):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method")

    rental_days = request.POST.get("rental_days")
    if not rental_days:
        return HttpResponseBadRequest("Rental days not provided")

    try:
        rental_days = int(rental_days)
        if rental_days <= 0:
            raise ValueError
    except ValueError:
        return HttpResponseBadRequest("Invalid rental days")

    # Chuyển book_id sang ObjectId
    try:
        obj_id = ObjectId(book_id)
    except:
        return HttpResponseBadRequest("Invalid book ID")

    book = get_object_or_404(Book, _id=obj_id)

    cart = request.session.get("cart", {})

    if book_id in cart:
        cart[book_id]["rental_days"] += rental_days
    else:
        cart[book_id] = {
            "title": book.title,
            "rental_price_per_day": float(book.rental_price_per_day),
            "rental_days": rental_days
        }

    request.session["cart"] = cart
    request.session.modified = True
    return redirect('cart')


def cart(request):
    cart = request.session.get("cart", {})
    cart_items_with_subtotal = []
    total = 0

    for book_id, item in cart.items():
        subtotal = item["rental_price_per_day"] * item["rental_days"]
        total += subtotal
        item["subtotal"] = subtotal
        item["book_id"] = book_id
        cart_items_with_subtotal.append(item)

    cart_count = len(cart_items_with_subtotal)

    context = {
        "cart_items": cart_items_with_subtotal,
        "total": total,
        "cart_count": cart_count,
    }
    return render(request, 'books/cart.html', context)


def remove_from_cart(request, item_id):
    cart = request.session.get("cart", {})
    if item_id in cart:
        del cart[item_id]
        request.session["cart"] = cart
        request.session.modified = True
    return redirect('cart')


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Giỏ hàng trống!')
        return redirect('cart')

    total = sum(item["rental_price_per_day"] * item["rental_days"] for item in cart.values())
    context = {
        'cart_items': cart.values(),
        'total': total,
        'cart_count': len(cart),
    }
    return render(request, 'books/checkout.html', context)


def process_order(request):
    if request.method != 'POST':
        return redirect('checkout')

    # 1. Lấy thông tin khách hàng
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    payment_method = request.POST.get('payment_method')

    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Giỏ hàng trống!')
        return redirect('cart')

    # 2. Tính tổng tiền
    total = sum(float(item["rental_price_per_day"]) * int(item["rental_days"]) for item in cart.values())

    # 3. Tạo order_number
    order_number = 'ORD' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    # 4. Tạo Order trong MongoDB
    order_data = {
        '_id': ObjectId(),
        'id': uuid.uuid4().hex,
        'order_number': order_number,
        'customer_name': name,
        'customer_email': email,
        'customer_phone': phone,
        'customer_address': address,
        'total_amount': float(total),
        'payment_method': payment_method,
        'status': 'confirmed',
        'created_at': datetime.now()
    }
    order_result = mongo_db.orders.insert_one(order_data)
    order_id = order_result.inserted_id

    # 5. Tạo OrderItems và Rentals
    for book_id, item in cart.items():
        # 5a. OrderItem
        order_item_data = {
            '_id': ObjectId(),
            'id': uuid.uuid4().hex,
            'order_id': str(order_id),
            'book_id': book_id,
            'book_title': item['title'],
            'rental_days': int(item['rental_days']),
            'price_per_day': float(item['rental_price_per_day']),
            'subtotal': float(item['rental_price_per_day']) * int(item['rental_days'])
        }
        mongo_db.order_items.insert_one(order_item_data)

        # 5b. Rental
        try:
            book = mongo_db.books.find_one({'_id': ObjectId(book_id)})
            if book:
                expected_return = datetime.now() + timedelta(days=int(item['rental_days']))
                rental_data = {
                    'order_id': str(order_id),
                    'order_number': order_number,
                    'book_id': book_id,
                    'book_title': item['title'],
                    'book_cover': book.get('cover_image', ''),
                    'customer_name': name,
                    'customer_email': email,
                    'rental_days': int(item['rental_days']),
                    'price_per_day': float(item['rental_price_per_day']),
                    'total_cost': float(item['rental_price_per_day']) * int(item['rental_days']),
                    'rental_date': datetime.now(),
                    'expected_return_date': expected_return,
                    'actual_return_date': None,
                    'status': 'active',
                    'late_fee': 0.0,
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                }
                mongo_db.rentals.insert_one(rental_data)

                # Giảm số lượng sách
                mongo_db.books.update_one(
                    {'_id': ObjectId(book_id)},
                    {'$inc': {'available_copies': -1}}
                )
        except Exception as e:
            print(f"Lỗi khi tạo rental: {e}")

    # 6. Xóa cart
    request.session['cart'] = {}
    request.session.modified = True

    messages.success(request, f'Đặt hàng thành công! Mã đơn hàng: {order_number}')
    return redirect('order_success', order_id=str(order_id))

    return redirect('checkout')


def order_success(request, order_id):
    try:
        # Lấy order từ MongoDB
        order = mongo_db.orders.find_one({'_id': ObjectId(order_id)})

        if not order:
            messages.error(request, 'Không tìm thấy đơn hàng!')
            return redirect('homepage')

        # Lấy order items
        order_items = list(mongo_db.order_items.find({'order_id': str(order_id)}))

        context = {
            'order': order,
            'order_items': order_items,
            'cart_count': 0,
        }
        return render(request, 'books/order_success.html', context)

    except Exception as e:
        messages.error(request, f'Lỗi: {str(e)}')
        return redirect('homepage')
def my_rentals(request):
    if not request.user.is_authenticated:
        messages.error(request, "Vui lòng đăng nhập!")
        return redirect('accounts:login')

    active_rentals = Rental.objects.filter(customer_email=request.user.email, status='active')
    for r in active_rentals:
        if r.is_overdue():
            r.status = 'overdue'
            r.late_fee = r.calculate_late_fee()
            r.save()

    active_rentals = Rental.objects.filter(customer_email=request.user.email, status__in=['active','overdue'])
    returned_rentals = Rental.objects.filter(customer_email=request.user.email, status='returned')
    session_id = get_session_id(request)
    cart_count = CartItem.objects.filter(session_id=session_id).count()

    context = {
        "active_rentals": active_rentals,
        "returned_rentals": returned_rentals,
        "cart_count": cart_count,
    }
    return render(request, "books/my_rentals.html", context)


def return_book(request, rental_id):
    if not request.user.is_authenticated:
        messages.error(request, "Vui lòng đăng nhập!")
        return redirect('accounts:login')

    try:
        rental_obj_id = ObjectId(rental_id)
    except:
        messages.error(request, "ID thuê sách không hợp lệ!")
        return redirect('my_rentals')

    rental = mongo_db.rentals.find_one({'_id': rental_obj_id, 'customer_email': request.user.email})
    if not rental:
        messages.error(request, "Không tìm thấy thuê sách này!")
        return redirect('my_rentals')

    if rental.get('status') == 'returned':
        messages.warning(request, "Sách này đã được trả rồi!")
        return redirect('my_rentals')

    # Cập nhật rental
    late_fee = 0
    now = timezone.now()
    expected_return = rental.get('expected_return_date')
    if expected_return and now > expected_return:
        days_overdue = (now - expected_return).days
        late_fee = days_overdue * 10  # ví dụ 10k/ngày

    mongo_db.rentals.update_one(
        {'_id': rental_obj_id},
        {'$set': {
            'status': 'returned',
            'actual_return_date': now,
            'late_fee': late_fee
        }}
    )

    try:
        book_id = ObjectId(rental.get('book_id'))
        book = Book.objects.get(_id=book_id)
        book.available_copies += 1
        book.save()
    except:
        pass

    if late_fee > 0:
        messages.warning(request, f'Đã trả sách "{rental.get("book_title")}". Phí trễ hạn: {late_fee}k VNĐ')
    else:
        messages.success(request, f'Đã trả sách "{rental.get("book_title")}" thành công!')

    return redirect('my_rentals')
