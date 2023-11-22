from rest_framework import serializers as s
from catalog.models import Book, BookInstance, Author


class BookSerializer(s.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'summary',
                  'isbn', 'genre', 'language')
        extra_kwargs = {
            'genre': {'required': False}
        }
