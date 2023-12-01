import pytest

from users.models import User


@pytest.fixture
def a_strong_password():
    return 'AStrong!@#123Password'


@pytest.mark.django_db
@pytest.fixture
def user01(a_strong_password) -> User:
    user = User.objects.create_user(
        username='user01',
        email='user01@email.com',
        password=a_strong_password
    )
    yield user


@pytest.mark.django_db
@pytest.fixture
def user02(a_strong_password) -> User:
    user = User.objects.create_user(
        username='user02',
        email='user02@email.com',
        password=a_strong_password
    )
    yield user


@pytest.mark.django_db
@pytest.fixture
def insert_2_users(user01, user02):
    yield user01, user02
