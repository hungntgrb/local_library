import pytest

from django.test import Client
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
class TestUserLoginAPI:

    def api_login_post(self, client_, data=None):
        if data is None:
            data = {
                'email': 'an-email-address',
                'password': 'a-strong-password'
            }

        return client_.post(
            reverse('users_api:login'),
            data=data,
            content_type='application/json'
        )

    def test_there_are_2_users(self):
        assert User.objects.count() == 2

    def test_guest_login(self, client: Client,
                         user_test_1, astrongpassword):
        res = self.api_login_post(
            client,
            data={
                'email': user_test_1.email,
                'password': astrongpassword
            }
        )

        assert res.status_code == 200

        for key in ('id', 'username', 'email',
                    'first_name', 'last_name', 'is_staff'):
            assert key in res.json()

    def test_guest_login_bad_data(self, client: Client,
                                  user_test_1, astrongpassword):
        res = self.api_login_post(
            client,
            data={
                'email': user_test_1.email
            }
        )

        assert res.status_code == 400

    def test_guest_login_wrong_password(self, client: Client,
                                        user_test_1):
        res = self.api_login_post(
            client,
            data={
                'email': user_test_1.email,
                'password': 'a_wrong_password'
            }
        )

        assert res.status_code == 404
        assert res.json() == {'detail': 'Please check email and password!'}

    def test_user1_login(self, client: Client,
                         user_test_1, astrongpassword):
        client.force_login(user_test_1)

        res = self.api_login_post(
            client,
            data={
                'email': user_test_1.email,
                'password': astrongpassword
            }
        )

        assert res.status_code == 403
        assert res.json() == {'detail': 'User already logged-in.'}
