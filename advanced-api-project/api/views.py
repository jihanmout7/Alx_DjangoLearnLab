from django.shortcuts import render
from rest_framework import generics
from .models import Book 
from .serializers import BookSerializer
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication 
# Create your views here.

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
class BookList(generics.DetailAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookList(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']
    
    permission_classes = [IsAuthenticated]  # Only authenticated admin users

    
class BookList(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    search_fields = ['title']
    permission_classes = [IsAuthenticated]  # Only authenticated admin users

class BookList(generics.DeleteAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated admin users
    
