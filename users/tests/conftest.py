import pytest

from users.models import User


@pytest.fixture
def astrongpassword():
    return 'AStrong!@#123Password'


@pytest.mark.django_db()
@pytest.fixture
def user_test_1(astrongpassword) -> User:
    user1 = User.objects.create_user(
        username=f'user_test_1',
        email=f'user_test_1@email.com',
        password=astrongpassword
    )
    yield user1


@pytest.mark.django_db()
@pytest.fixture
def user_test_2(astrongpassword) -> User:
    user2 = User.objects.create_user(
        username=f'user_test_2',
        email=f'user_test_2@email.com',
        password=astrongpassword
    )
    yield user2
