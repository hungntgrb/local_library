import pytest

from django.urls import reverse
from users.models import User


@pytest.mark.django_db()
class TestUserRegisterAPI:

    @pytest.mark.parametrize("user_data, status_code", (
        ({"": ""}, 400),
        ({"username": "user1"}, 400),
        ({
            "username": "user1",
            "email": "user1@email.com"
        }, 400),
        ({
            "username": "user1",
            "password": "AStrongPassword"
        }, 400),
        ({"password": "AStrongPassword"}, 400),
        ({"email": "user1@email.com"}, 400),
        ({
            "email": "user1@email.com",
            "password": "AStrongPassword"
        }, 400),
        ({
            "email": "user1@email.com",
            "password": "shortpwd"
        }, 400),
        ({
            "username": "user1",
            "email": "user1@email.com",
            "password": "AStrongPassword"
        }, 201),
    ))
    def test_return_proper_status_code_according_data(
        self, client, user_data, status_code
    ):
        user_register_api_endpoint = reverse('users_api:user_create')

        res = client.post(
            user_register_api_endpoint,
            data=user_data,
            content_type='application/json')

        assert res.status_code == status_code, 'Status khong khop!'


@pytest.mark.django_db()
@pytest.mark.usefixtures('populate_2_users')
class TestUserAuthAPI:
    def test_there_are_2_users(self):
        assert User.objects.count() == 2

    def test_register_user_there_are_3_users(self, client, astrongpassword):
        res = client.post(
            reverse('users_api:user_create'),
            data={
                'username': 'user_test_03',
                'email': 'user_test_03@email.com',
                'password': astrongpassword
            },
            content_type='application/json'
        )

        assert res.status_code == 201
        assert User.objects.count() == 3

    def test_user_login(self, client, astrongpassword):
        res = client.post(
            reverse('users_api:login'),
            data={
                'email': 'user_test_01@email.com',
                'password': astrongpassword
            },
            content_type='application/json'
        )
        assert res.status_code == 200

        for key in ('id', 'username', 'email',
                    'first_name', 'last_name', 'is_staff'):
            assert key in res.json()

    # def test_user_logout(self):
    #     pass
