import pytest

from catalog.models import Book, Author, BookInstance
from users.models import User
from django.contrib.auth.models import Group, Permission


# ===================================================
#                     Books
# ===================================================


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
def insert_2_available_instances(insert_2_books):
    book1, book2 = insert_2_books
    b1i1a = BookInstance.objects.create(book=book1, status='a')
    b2i1a = BookInstance.objects.create(book=book2, status='a')
    yield b1i1a,  b2i1a


@pytest.mark.django_db
@pytest.fixture
def insert_2_on_loan_instances(insert_2_books, user01):
    book1, book2 = insert_2_books
    b1i1o = BookInstance.objects.create(book=book1, status='o',
                                        borrower=user01)
    b2i1o = BookInstance.objects.create(book=book2, status='o',
                                        borrower=user01)
    yield b1i1o,  b2i1o


@pytest.mark.django_db
@pytest.fixture
def insert_2_maintaining_instances(insert_2_books):
    book1, book2 = insert_2_books
    b1i1m = BookInstance.objects.create(book=book1, status='m')
    b2i1m = BookInstance.objects.create(book=book2, status='m')
    yield b1i1m,  b2i1m


@pytest.mark.django_db
@pytest.fixture
def insert_some_instances(insert_2_available_instances,
                          insert_2_on_loan_instances,
                          insert_2_maintaining_instances):
    b1i1a, b2i1a = insert_2_available_instances
    b1i2o, b2i2o = insert_2_on_loan_instances
    b1i3m, b2i3m = insert_2_maintaining_instances
    yield b1i1a, b1i2o, b1i3m, b2i1a, b2i2o, b2i3m


# ===================================================
#                      Users
# ===================================================


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


# ===================================================
#                    Authors
# ===================================================


@pytest.mark.django_db
@pytest.fixture
def author_1():
    _author = Author.objects.create(
        first_name='Hung',
        last_name='Nguyen'
    )
    yield _author


@pytest.fixture
def expected_author_1_data():
    _data = {
        'first_name': 'Hung',
        'last_name': 'Nguyen',
        'date_of_birth': None,
        'date_of_death': None,
    }
    yield _data
