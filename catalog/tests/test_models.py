from django.test import TestCase
from datetime import date, timedelta
from mixer.backend.django import mixer
import pytest

from catalog.models import Author


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a model for testing
        Author.objects.create(first_name="Ken", last_name="Miles")

    def setUp(self):
        self.author = Author.objects.get(pk=1)

    def test_first_name_label(self):
        expected_label = self.author._meta.get_field("first_name").verbose_name
        self.assertEqual(expected_label, "first name")

    def test_date_of_death_label(self):
        expected_label = self.author._meta.get_field("date_of_death").verbose_name
        self.assertEqual(expected_label, "Died")

    def test_first_name_max_length(self):
        max_length = self.author._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 100)

    def test_author_name_is_last_name_comma_first_name(self):
        expected_name = f"{self.author.last_name}, {self.author.first_name}"
        self.assertEqual(expected_name, str(self.author))

    def test_object_get_absolute_url(self):
        self.assertEqual(self.author.get_absolute_url(), "/catalog/author/1")

    def test_last_name_label(self):
        last_name_label = self.author._meta.get_field("last_name").verbose_name
        self.assertEqual(last_name_label, "last name")

    def test_last_name_max_length(self):
        max_length = self.author._meta.get_field("last_name").max_length
        self.assertEqual(max_length, 100)


@pytest.mark.django_db
class TestBookInstance:
    _3_days_ago = date.today() - timedelta(days=3)
    today = date.today()
    _3_days_ahead = date.today() + timedelta(days=3)

    def a_copy_dueback_on(self, someday):
        return mixer.blend("catalog.BookInstance", due_back=someday)

    def test_a_copy_is_overdue(self):
        assert self.a_copy_dueback_on(self._3_days_ago).is_overdue == True

    def test_a_copy_is_not_overdue_when_duedate_is_today(self):
        assert self.a_copy_dueback_on(self.today).is_overdue == False

    def test_a_copy_is_not_overdue_when_duedate_is_3_days_ahead(self):
        assert self.a_copy_dueback_on(self._3_days_ahead).is_overdue == False
