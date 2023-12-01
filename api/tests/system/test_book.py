import pytest

from django.urls import reverse
from django.test.client import Client

from catalog.models import Book, BookInstance


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


@pytest.mark.django_db
@pytest.mark.usefixtures('insert_1_book')
class TestRetrieveABook:

    def api_retrieve_a_book(self, client_, book_id):
        return client_.get(reverse(
            'api:book_retrieve', kwargs={'pk': book_id})
        )

    def test_a_book_does_not_exist(self, client: Client,
                                   insert_1_book):
        book1 = insert_1_book
        res = self.api_retrieve_a_book(client,
                                       book_id='a1d3s2f4g6f5d4')

        assert res.status_code == 404

    def test_anonymous_user_get_a_book(self, client: Client,
                                       insert_1_book):
        book1 = insert_1_book
        res = self.api_retrieve_a_book(client,
                                       book_id=book1.id)

        assert res.status_code == 200

    def test_normal_user_get_a_book(self, client: Client,
                                    insert_1_book, normal_user_1):
        book1 = insert_1_book
        client.force_login(normal_user_1)

        res = self.api_retrieve_a_book(client,
                                       book_id=book1.id)

        assert res.status_code == 200

    def test_staff_user_get_a_book(self, client: Client,
                                   insert_1_book, staff_user_1):
        book1 = insert_1_book
        client.force_login(staff_user_1)

        res = self.api_retrieve_a_book(client,
                                       book_id=book1.id)

        assert res.status_code == 200


@pytest.mark.django_db
@pytest.mark.usefixtures('insert_2_available_instances',
                         'insert_2_on_loan_instances')
class TestBorrowABook:
    def test_there_are_2_available_instances(self):
        assert BookInstance.objects.filter(status='a').count() == 2

    def test_there_are_2_on_loan_instances(self):
        assert BookInstance.objects.filter(status='o').count() == 2

    def api_borrow_a_book(self, client_, instance_id):
        return client_.get(
            reverse('api:borrow_a_book',
                    kwargs={'instance_id': instance_id}),
        )

    def test_anonymous_cannot_borrow(self, client: Client,
                                     insert_2_available_instances):
        b1a, b2a = insert_2_available_instances

        res = self.api_borrow_a_book(client, b1a.id)

        assert res.status_code == 403

    def test_user_borrow_an_available(self, client: Client, user01,
                                      insert_2_available_instances):
        b1a, b2a = insert_2_available_instances

        client.force_login(user01)
        res = self.api_borrow_a_book(client, b1a.id)

        assert res.status_code == 200

    def test_user_borrow_an_on_loan(self, client: Client, user02,
                                    insert_2_on_loan_instances):
        b1o, b2o = insert_2_on_loan_instances

        client.force_login(user02)
        res = self.api_borrow_a_book(client, b1o.id)

        assert res.status_code == 400

    def test_user_borrow_a_maintaining(self, client: Client, user02,
                                       insert_2_maintaining_instances):
        b1m, b2m = insert_2_maintaining_instances

        client.force_login(user02)
        res = self.api_borrow_a_book(client, b1m.id)

        assert res.status_code == 400

    def test_user_borrow_a_non_existing(self, client: Client, user02):

        client.force_login(user02)
        res = self.api_borrow_a_book(client,
                                     'f4dbe637-57fe-463b-8d60-c757dccccccc')

        assert res.status_code == 404
