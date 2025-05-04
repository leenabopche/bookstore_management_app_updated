from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # No Django admin as per instructions
    path('', include('bookstore_app.urls')),
]
