from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Book
from django.contrib import messages

# Helper function for manual form validation
def validate_registration_form(data):
    errors = []
    if not data.get('username'):
        errors.append('Username is required.')
    if not data.get('password'):
        errors.append('Password is required.')
    if data.get('password') != data.get('password_confirm'):
        errors.append('Passwords do not match.')
    if User.objects.filter(username=data.get('username')).exists():
        errors.append('Username already exists.')
    return errors

class UserRegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        data = request.POST
        errors = validate_registration_form(data)
        if errors:
            return render(request, 'register.html', {'errors': errors, 'data': data})
        user = User.objects.create_user(username=data['username'], password=data['password'])
        messages.success(request, 'Registration successful. Please login.')
        return redirect('bookstore_app:login')

class UserLoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('bookstore_app:book_list')
        else:
            error = 'Invalid username or password.'
            return render(request, 'login.html', {'error': error})

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('bookstore_app:login')

class BookListView(View):
    def get(self, request):
        books = Book.objects.all()
        cart = request.session.get('cart', {})
        cart_item_count = sum(cart.values())
        return render(request, 'book_list.html', {'books': books, 'cart_item_count': cart_item_count})

class BookDetailView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'book_detail.html', {'book': book})

class AddToCartView(View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        cart = request.session.get('cart', {})
        if str(pk) in cart:
            cart[str(pk)] += 1
        else:
            cart[str(pk)] = 1
        request.session['cart'] = cart
        messages.success(request, f'Added {book.title} to cart.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('bookstore_app:book_list')))

class CartView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        books = []
        total = 0
        for book_id, quantity in cart.items():
            book = get_object_or_404(Book, pk=book_id)
            books.append({'book': book, 'quantity': quantity, 'subtotal': book.price * quantity})
            total += book.price * quantity
        return render(request, 'cart.html', {'cart_items': books, 'total': total})

# Admin Panel Views

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('bookstore_app:login')
        return view_func(request, *args, **kwargs)
    return wrapper

class AdminBookListView(View):
    @admin_required
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'admin/book_list.html', {'books': books})

class AdminBookCreateView(View):
    @admin_required
    def get(self, request):
        return render(request, 'admin/book_form.html')

    @admin_required
    def post(self, request):
        data = request.POST
        title = data.get('title')
        author = data.get('author')
        description = data.get('description')
        price = data.get('price')
        stock = data.get('stock')
        errors = []
        if not title:
            errors.append('Title is required.')
        if not author:
            errors.append('Author is required.')
        try:
            price = float(price)
            if price < 0:
                errors.append('Price must be non-negative.')
        except (ValueError, TypeError):
            errors.append('Invalid price.')
        try:
            stock = int(stock)
            if stock < 0:
                errors.append('Stock must be non-negative.')
        except (ValueError, TypeError):
            errors.append('Invalid stock.')
        if errors:
            return render(request, 'admin/book_form.html', {'errors': errors, 'data': data})
        Book.objects.create(title=title, author=author, description=description, price=price, stock=stock)
        messages.success(request, 'Book added successfully.')
        return redirect('bookstore_app:admin_book_list')

class AdminBookUpdateView(View):
    @admin_required
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'admin/book_form.html', {'data': book})

    @admin_required
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        data = request.POST
        title = data.get('title')
        author = data.get('author')
        description = data.get('description')
        price = data.get('price')
        stock = data.get('stock')
        errors = []
        if not title:
            errors.append('Title is required.')
        if not author:
            errors.append('Author is required.')
        try:
            price = float(price)
            if price < 0:
                errors.append('Price must be non-negative.')
        except (ValueError, TypeError):
            errors.append('Invalid price.')
        try:
            stock = int(stock)
            if stock < 0:
                errors.append('Stock must be non-negative.')
        except (ValueError, TypeError):
            errors.append('Invalid stock.')
        if errors:
            return render(request, 'admin/book_form.html', {'errors': errors, 'data': data})
        book.title = title
        book.author = author
        book.description = description
        book.price = price
        book.stock = stock
        book.save()
        messages.success(request, 'Book updated successfully.')
        return redirect('bookstore_app:admin_book_list')

class AdminBookDeleteView(View):
    @admin_required
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        messages.success(request, 'Book deleted successfully.')
        return redirect('bookstore_app:admin_book_list')
