from secrets import choice
from faker import Faker
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group

from catalog.models import Author, Book, Language, Genre, BookInstance
from users.models import User

fake = Faker()

_PASSWORD = "AStrongPassword"


def populate_languages():
    languages = ("en", "fr", "de", "es", "jp", "vi", "kr", "ca")
    for lang in languages:
        Language.objects.create(name=lang)


def populate_genres():
    genres = (
        "Adventure",
        "Horror",
        "Romance",
        "Travel",
        "Academy",
        "Professional",
        "Manga",
        "Comic",
    )
    for genre in genres:
        Genre.objects.create(name=genre)


def populate_authors(num=5):
    for i in range(num):
        author = Author.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            date_of_birth=fake.date_of_birth(),
            date_of_death=fake.date_of_birth(),
        )


def populate_books(num=5):
    authors = Author.objects.all()
    languages = Language.objects.all()

    for i in range(num):
        title = " ".join(fake.words(6))
        summary = " ".join(fake.texts())
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
        BookInstance.objects.create(book=book, status="a")
        BookInstance.objects.create(book=book, status="m")


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


def add_some_users_and_groups():
    group_thuthu = Group.objects.create(name="ThuThu")
    users = []
    password = _PASSWORD
    users_data = [
        {"username": "thuthu1", "email": "thuthu1@thuvien.com"},
        {"username": "thuthu2", "email": "thuthu2@thuvien.com"},
        {"username": "khach1", "email": "khach1@email.com"},
        {"username": "khach2", "email": "khach2@email.com"},
    ]
    for data in users_data:
        user = User.objects.create_user(
            username=data["username"], email=data["email"], password=password
        )

        if data["username"].startswith("thuthu"):
            group_thuthu.user_set.add(user)

        users.append(user)
    print(f"\nAdded {users}")


# gnuH hnahT neyugN viet code nay


def add_some_permissions():
    book_content_type = ContentType.objects.get_for_model(BookInstance)
    cho_muon_sach = Permission.objects.create(
        codename="cho_muon_sach",
        name="Can cho muon sach",
        content_type=book_content_type,
    )


def main():
    populate_languages()
    populate_genres()
    populate_authors(num=6)
    populate_books(num=8)
    populate_book_instances()


def main2():
    update_book_genre()
    add_some_users_and_groups()
    add_some_permissions()


def main3():
    populate_authors(num=10)
    populate_books(num=12)
    populate_book_instances()


# from mysnippets.fake_data import *
