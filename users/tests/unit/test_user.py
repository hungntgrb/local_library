import pytest

from users.models import User


@pytest.mark.django_db
class TestUser:
    def test_create_user(self, astrongpassword):
        user = User.objects.create_user(
            username='user01',
            email='user01@email.com',
            password=astrongpassword
        )
        assert User.objects.count() == 1
        assert User.objects.first().is_staff == False

    def test_create_staff_user(self, astrongpassword):
        user = User.objects.create_staff(
            username='user01',
            email='user01@email.com',
            password=astrongpassword
        )
        assert User.objects.count() == 1
        user1 = User.objects.first()
        assert user1.is_staff
        assert user1.username == 'user01'
        assert user1.email == 'user01@email.com'
        assert user1.check_password(astrongpassword)
