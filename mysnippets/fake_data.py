from secrets import choice
from faker import Faker

from catalog.models import (Author, Book, Language, Genre, BookInstance)

fake = Faker()


def populate_languages():
    languages = ('en', 'fr', 'de', 'es', 'jp', 'vi', 'kr', 'ca')
    for lang in languages:
        Language.objects.create(
            name=lang
        )


def populate_genres():
    genres = ('Adventure', 'Horror', 'Romance', 'Travel',
              'Academy', 'Professional', 'Manga', 'Comic')
    for genre in genres:
        Genre.objects.create(
            name=genre
        )


def populate_authors(num=5):
    for i in range(num):
        author = Author.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            date_of_birth=fake.date_of_birth(),
            date_of_death=fake.date_of_birth()
        )


def populate_books(num=5):
    authors = Author.objects.all()
    languages = Language.objects.all()

    for i in range(num):
        title = ' '.join(fake.words(6))
        summary = ' '.join(fake.texts())
        Book.objects.create(
            title=title,
            summary=summary,
            author=choice(authors),
            isbn=fake.isbn10(),
            language=choice(languages),
        )


def populate_book_instances():
    books = Book.objects.all()

    for book in books:
        BookInstance.objects.create(
            book=book,
            status='a'
        )
        BookInstance.objects.create(
            book=book,
            status='m'
        )


def update_book_genre():
    books = Book.objects.all()
    genres = Genre.objects.all()
    for book in books:
        book.genre.set([choice(genres), choice(genres)])
        book.save()


def delete_books():
    Book.objects.all().delete()


def delete_authors():
    Author.objects.all().delete()


def delete_book_instances():
    BookInstance.objects.all().delete()


def main():
    pass

# from mysnippets.fake_data import *
