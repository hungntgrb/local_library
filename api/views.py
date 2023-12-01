from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.permissions import (AllowAny, IsAdminUser,
                                        IsAuthenticated)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from catalog.models import Book, Author, BookInstance
from api.serializers import BookSerializer, AuthorSerializer
from .permissions import IsLibrarianOrAdmin
from catalog import actions as a


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
# ===================================================
#                   Authors
# ===================================================


class AuthorListAPIView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (AllowAny,)


author_list = AuthorListAPIView.as_view()


class AuthorCreateAPIView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsLibrarianOrAdmin,)


author_create = AuthorCreateAPIView.as_view()


class AuthorRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (AllowAny,)


author_retrieve = AuthorRetrieveAPIView.as_view()


class AuthorUpdateAPIView(generics.UpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsLibrarianOrAdmin,)


author_update = AuthorUpdateAPIView.as_view()


class AuthorDestroyAPIView(generics.DestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsAdminUser,)


author_destroy = AuthorDestroyAPIView.as_view()


@api_view(('GET',))
@permission_classes((IsAuthenticated,))
def borrow_a_book(request, instance_id, *args, **kwargs):
    instance = get_object_or_404(BookInstance, id=instance_id)
    book_title = instance.book.title

    if not instance.is_available:
        return Response({'detail': f'Book "{book_title}" is not available right now.'},
                        status=status.HTTP_400_BAD_REQUEST)

    a.mark_book_as_on_loan(instance, request.user)

    return Response({'detail': f'Borrowed "{book_title}" successfully!'})
