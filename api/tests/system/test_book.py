import pytest

from django.urls import reverse
from django.test.client import Client

from catalog.models import Book


@pytest.mark.django_db
class TestCreateABook:
    def post_a_book_json_data(self, client_):
        return client_.post(
            reverse('api:book_create'),
            data={
                'title': 'The Book 1',
                'summary': 'The Summary 1',
                'isbn': '9783737505536'
            },
            content_type='application/json'
        )

    def test_anonymous_user_cannot_create_book(self, client: Client):
        res = self.post_a_book_json_data(client)
        assert res.status_code == 403
        assert Book.objects.count() == 0

    def test_normal_user_cannot_create_book(self,
                                            client: Client,
                                            normal_user_1):
        client.force_login(normal_user_1)

        res = self.post_a_book_json_data(client)
        assert res.status_code == 403
        assert Book.objects.count() == 0

    def test_librarian_can_create_book(self,
                                       client: Client,
                                       librarian_1):
        assert librarian_1.has_perm('catalog.add_book')

        client.force_login(librarian_1)

        res = self.post_a_book_json_data(client)
        assert res.status_code == 201
        assert Book.objects.count() == 1

    def test_staff_can_create_book(self,
                                   client: Client,
                                   staff_user_1):
        client.force_login(staff_user_1)

        res = self.post_a_book_json_data(client)
        assert res.status_code == 201
        assert Book.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.usefixtures('insert_1_book')
class TestRetrieveBookList:
    def api_get_book_list(self, client_):
        return client_.get(
            reverse('api:book_list'),
        )

    def test_1_books_exists(self, client):
        res = self.api_get_book_list(client)

        assert res.status_code == 200
        res_data = res.json()
        assert len(res_data) == 1
        assert res_data[0]['title'] == 'Book 001'
        assert res_data[0]['summary'] == 'Summary 001'

    def test_2_books_exist(self, client, insert_2_books):
        res = self.api_get_book_list(client)

        assert res.status_code == 200
        res_data = res.json()
        assert len(res_data) == 2

    def test_insert_3rd_book(self, client, insert_2_books):
        Book.objects.create(
            title='Book 003',
            summary='Summary 003'
        )
        res = self.api_get_book_list(client)

        assert res.status_code == 200
        res_data = res.json()
        assert len(res_data) == 3

    def test_anonymous_user_get_book_list(self, client: Client, insert_2_books):
        res = self.api_get_book_list(client)

        assert res.status_code == 200
        res_data = res.json()
        assert len(res_data) == 2

    def test_normal_user_get_book_list(self, client: Client,
                                       insert_2_books, normal_user_1):
        client.force_login(normal_user_1)

        res = self.api_get_book_list(client)

        assert res.status_code == 200
        res_data = res.json()
        assert len(res_data) == 2

    def test_staff_user_get_book_list(self, client: Client,
                                      insert_2_books, staff_user_1):
        client.force_login(staff_user_1)

        res = self.api_get_book_list(client)

        assert res.status_code == 200
        res_data = res.json()
        assert len(res_data) == 2
