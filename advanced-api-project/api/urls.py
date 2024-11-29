from django.urls import path, include
from .models import Book
from .serializers import BookSerializer
from .views import BookList


urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),

]
