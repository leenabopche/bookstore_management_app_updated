from django.urls import path
from .views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    BookListView,
    BookDetailView,
    AddToCartView,
    CartView,
    AdminBookListView,
    AdminBookCreateView,
    AdminBookUpdateView,
    AdminBookDeleteView,
)

app_name = 'bookstore_app'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('', BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('add-to-cart/<int:pk>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),

    # Admin panel URLs
    path('admin/books/', AdminBookListView.as_view(), name='admin_book_list'),
    path('admin/books/add/', AdminBookCreateView.as_view(), name='admin_book_add'),
    path('admin/books/<int:pk>/edit/', AdminBookUpdateView.as_view(), name='admin_book_edit'),
    path('admin/books/<int:pk>/delete/', AdminBookDeleteView.as_view(), name='admin_book_delete'),
]
