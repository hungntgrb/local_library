import pytest

from catalog.models import Book
from users.models import User
from django.contrib.auth.models import Group, Permission


@pytest.mark.django_db
@pytest.fixture
def insert_1_book():
    book1 = Book.objects.create(
        title='Book 001',
        summary='Summary 001'
    )
    # print('\n--- insert_1_book()')
    yield book1


@pytest.mark.django_db
@pytest.fixture
def insert_2_books(insert_1_book):
    book1 = insert_1_book
    book2 = Book.objects.create(
        title='Book 002',
        summary='Summary 002'
    )
    # print('\n--- insert_1_more_book()')
    yield book1, book2


@pytest.mark.django_db
@pytest.fixture
def normal_user_1(a_strong_password):
    user = User.objects.create_user(
        username='normal_user_1',
        email='normal_user_1@library.com',
        password=a_strong_password
    )
    yield user


@pytest.mark.django_db
@pytest.fixture
def librarian_1(a_strong_password):
    add_book = Permission.objects.get(codename='add_book')
    thuthu = Group.objects.create(name='ThuThu')
    thuthu.permissions.add(add_book)

    user = User.objects.create_user(
        username='librarian_1',
        email='librarian_1@library.com',
        password=a_strong_password
    )
    user.groups.add(thuthu)

    yield user


@pytest.mark.django_db
@pytest.fixture
def staff_user_1(a_strong_password):
    user = User.objects.create_user(
        username='staff_user_1',
        email='staff_user_1@library.com',
        password=a_strong_password
    )
    user.is_staff = True
    user.save()
    yield user


@pytest.mark.django_db
@pytest.fixture
def insert_3_users(normal_user_1, librarian_1, staff_user_1):
    yield normal_user_1, librarian_1, staff_user_1
