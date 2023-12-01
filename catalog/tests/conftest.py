import pytest

from catalog.models import Book, BookInstance
from users.models import User


@pytest.fixture
def a_strong_password():
    return 'AStrong!@#123Password'


@pytest.mark.django_db
@pytest.fixture
def book1():
    book = Book.objects.create(title='Book Title 1',
                               summary='Book Summary 1')
    yield book


@pytest.mark.django_db
@pytest.fixture
def book2():
    book = Book.objects.create(title='Book Title 2',
                               summary='Book Summary 2')
    yield book


@pytest.mark.django_db
@pytest.fixture
def book1_available(book1):
    avail1 = BookInstance.objects.create(book=book1,
                                         status='a')
    yield avail1


@pytest.mark.django_db
@pytest.fixture
def book1_maintaining(book1):
    maint1 = BookInstance.objects.create(book=book1,
                                         status='m')
    yield maint1


@pytest.mark.django_db
@pytest.fixture
def book2_available(book2):
    avail2 = BookInstance.objects.create(book=book2,
                                         status='a')
    yield avail2


@pytest.mark.django_db
@pytest.fixture
def book2_maintaining(book2):
    maint2 = BookInstance.objects.create(book=book2,
                                         status='m')
    yield maint2


@pytest.mark.django_db
@pytest.fixture
def user1(a_strong_password):
    user = User.objects.create_user(
        username='user01',
        email='user01@email.com',
        password=a_strong_password
    )
    yield user
