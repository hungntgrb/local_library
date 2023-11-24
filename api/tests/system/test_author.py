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
