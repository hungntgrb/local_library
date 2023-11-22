import pytest

from users.models import User


@pytest.mark.django_db()
@pytest.fixture()
def populate_2_users(astrongpassword):
    for i in range(1, 3):
        User.objects.create_user(
            username=f'user_test_0{i}',
            email=f'user_test_0{i}@email.com',
            password=astrongpassword
        )
    yield
