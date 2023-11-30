import pytest

# from users.models import User


@pytest.mark.django_db()
@pytest.fixture()
def populate_2_users(user_test_1, user_test_2):

    yield user_test_1, user_test_2
