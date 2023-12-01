import pytest

from catalog.models import Book, Author


@pytest.mark.django_db()
class TestCreateABook:
    def test_minimal_data(self):
        book = Book.objects.create(
            title='Book Title 1',
            summary='Book summary 1'
        )
        assert Book.objects.count() == 1

    @pytest.mark.xfail
    def test_provide_wrong_argument(self):
        book = Book.objects.create(
            name='Book Title 1',
        )
        assert Book.objects.count() == 1

    def test_with_author(self):
        hung = Author.objects.create(
            first_name='Hung',
            last_name='Nguyen'
        )
        book = Book.objects.create(
            title='Book Title 1',
            summary='Book summary 1',
            author=hung
        )
        assert Book.objects.count() == 1
        assert Book.objects.first().author.first_name == 'Hung'

    @pytest.mark.xfail
    def test_isbn_too_long(self):
        book = Book.objects.create(
            title='Book Title 1',
            summary='Book summary 1',
            isbn='1234567890123456'
        )
        assert Book.objects.count() == 1
