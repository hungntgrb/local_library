from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser

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


class BookRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (AllowAny,)


book_retrieve = BookRetrieveAPIView.as_view()


class BookUpdateAPIView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsLibrarianOrAdmin,)


book_update = BookUpdateAPIView.as_view()


class BookDestroyAPIView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminUser,)


book_destroy = BookDestroyAPIView.as_view()
