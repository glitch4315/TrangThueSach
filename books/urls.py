from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('book/<str:book_id>/', views.book_detail, name='book_detail'),
    path('books/<str:filter_type>/', views.view_all_books, name='view_all_books'),
    path('add-to-cart/<str:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove-from-cart/<str:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('process-order/', views.process_order, name='process_order'),
    path('order-success/<str:order_id>/', views.order_success, name='order_success'),
]