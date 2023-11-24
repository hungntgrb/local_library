import pytest
from django.urls import reverse
from django.test import Client


@pytest.mark.django_db
@pytest.mark.usefixtures('author_1')
class TestAuthorList:
    def test_anonymous_user(self, client: Client,
                            expected_author_1_data):
        res = client.get(reverse('api:author_list'))

        assert res.status_code == 200
        res_json = res.json()
        assert len(res_json) == 1
        assert res_json[0] == expected_author_1_data

    def test_normal_user(self, client: Client,
                         normal_user_1, expected_author_1_data):
        client.force_login(normal_user_1)

        res = client.get(reverse('api:author_list'))

        assert res.status_code == 200
        res_json = res.json()
        assert len(res_json) == 1
        assert res_json[0] == expected_author_1_data

    def test_staff_user(self, client: Client,
                        staff_user_1, expected_author_1_data):
        client.force_login(staff_user_1)

        res = client.get(reverse('api:author_list'))

        assert res.status_code == 200
        res_json = res.json()
        assert len(res_json) == 1
        assert res_json[0] == expected_author_1_data


@pytest.mark.django_db
@pytest.mark.usefixtures('author_1')
class TestAuthorRetrieve:
    def api_author_retrieve(self, client_, author_pk):
        return client_.get(reverse(
            'api:author_retrieve', kwargs={'pk': author_pk}))

    def test_author_does_not_exist(self, client: Client):
        res = self.api_author_retrieve(client, 'doesnotexist')

        assert res.status_code == 404

    def test_anonymous_user(self, client: Client, author_1,
                            expected_author_1_data):
        res = self.api_author_retrieve(client, author_1.id)

        assert res.status_code == 200
        res_json = res.json()
        assert res_json == expected_author_1_data

    def test_normal_user(self, client: Client, author_1,
                         normal_user_1, expected_author_1_data):
        client.force_login(normal_user_1)

        res = self.api_author_retrieve(client, author_1.id)

        assert res.status_code == 200
        res_json = res.json()
        assert res_json == expected_author_1_data

    def test_staff_user(self, client: Client, author_1,
                        staff_user_1, expected_author_1_data):
        client.force_login(staff_user_1)

        res = self.api_author_retrieve(client, author_1.id)

        assert res.status_code == 200
        res_json = res.json()
        assert res_json == expected_author_1_data


@pytest.mark.django_db
class TestAuthorCreate:
    def api_author_create(self, client_, data=None):
        if data is None:
            data = {
                'first_name': 'Bruce',
                'last_name': 'Banner'
            }
        return client_.post(
            reverse('api:author_create'),
            data=data,
            content_type='application/json'
        )

    @property
    def expected_res_data(self):
        return {
            'first_name': 'Bruce',
            'last_name': 'Banner',
            'date_of_birth': None,
            'date_of_death': None,
        }

    def test_anonymous_user_cannot_create(self, client: Client):
        res = self.api_author_create(client)

        assert res.status_code == 403

    def test_librarian_can_create(self, client: Client,
                                  librarian_1):
        client.force_login(librarian_1)

        res = self.api_author_create(client)

        assert res.status_code == 201
        assert res.json() == self.expected_res_data

    def test_staff_user_can_create(self, client: Client,
                                   staff_user_1):
        client.force_login(staff_user_1)

        res = self.api_author_create(client)

        assert res.status_code == 201
        assert res.json() == self.expected_res_data

    def test_post_bad_data(self, client: Client,
                           librarian_1):
        client.force_login(librarian_1)

        res1 = self.api_author_create(client,
                                      data={'first_name': 'Libra'})

        assert res1.status_code == 400

        res2 = self.api_author_create(client,
                                      data={'last_name': 'Tran'})

        assert res2.status_code == 400


@pytest.mark.django_db
@pytest.mark.usefixtures('author_1')
class TestAuthorUpdate:

    @property
    def PUT_data(self):
        return {
            'first_name': 'Hung Updated',
            'last_name': 'Nguyen',
            'date_of_birth': None,
            'date_of_death': None,
        }

    @property
    def expected_res_data(self):
        return self.PUT_data

    def api_author_update(self, client_, author_pk, data=None):
        if data is None:
            data = self.PUT_data

        return client_.put(
            reverse(
                'api:author_update', kwargs={'pk': author_pk}),
            data=data,
            content_type='application/json'
        )

    def test_anonymous_user_cannot_update(self, client: Client, author_1):
        res = self.api_author_update(client, author_1.id)

        assert res.status_code == 403

    def test_normal_user_cannot_update(self, client: Client, author_1,
                                       normal_user_1):
        client.force_login(normal_user_1)

        res = self.api_author_update(client, author_1.id)

        assert res.status_code == 403

    def test_librarian_can_update(self, client: Client, author_1,
                                  librarian_1):
        client.force_login(librarian_1)

        res = self.api_author_update(client, author_1.id)

        assert res.status_code == 200
        assert res.json() == self.expected_res_data

    def test_author_does_not_exist(self, client: Client, librarian_1):
        client.force_login(librarian_1)

        res = self.api_author_update(client, 'doesnotexist')

        assert res.status_code == 404

    def test_staff_user_can_update(self, client: Client, author_1,
                                   staff_user_1):
        client.force_login(staff_user_1)

        res = self.api_author_update(client, author_1.id)

        assert res.status_code == 200
        assert res.json() == self.expected_res_data

    def test_PUT_bad_data(self, client: Client, author_1, librarian_1):
        client.force_login(librarian_1)

        res = self.api_author_update(client, author_1.id,
                                     data={'full_name': 'Spider Man'})

        assert res.status_code == 400


@pytest.mark.django_db
@pytest.mark.usefixtures('author_1')
class TestAuthorDestroy:

    def api_author_destroy(self, client_, author_pk):

        return client_.delete(
            reverse('api:author_destroy', kwargs={'pk': author_pk})
        )

    def test_anonymous_user_cannot_delete(self, client: Client, author_1):
        res = self.api_author_destroy(client, author_1.id)

        assert res.status_code == 403

    def test_normal_user_cannot_delete(self, client: Client, author_1,
                                       normal_user_1):
        client.force_login(normal_user_1)

        res = self.api_author_destroy(client, author_1.id)

        assert res.status_code == 403

    def test_librarian_cannot_delete(self, client: Client, author_1,
                                     librarian_1):
        client.force_login(librarian_1)

        res = self.api_author_destroy(client, author_1.id)

        assert res.status_code == 403

    def test_staff_user_can_delete(self, client: Client, author_1,
                                   staff_user_1):
        client.force_login(staff_user_1)

        res = self.api_author_destroy(client, author_1.id)

        assert res.status_code == 204

    def test_author_does_not_exist(self, client: Client, staff_user_1):
        client.force_login(staff_user_1)

        res = self.api_author_destroy(client, 'doesnotexist')

        assert res.status_code == 404
