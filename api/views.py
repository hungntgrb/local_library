from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from catalog.models import Book
from api.serializers import BookSerializer
from .permissions import IsLibrarianOrAdmin


class BookListPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (AllowAny,)


book_list = BookListPIView.as_view()


class BookCreateAPIView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsLibrarianOrAdmin,)


book_create = BookCreateAPIView.as_view()


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


book_rud = BookRetrieveUpdateDestroyAPIView.as_view()
