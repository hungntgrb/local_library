import pytest

from django.utils import timezone

from catalog import actions as a


@pytest.mark.django_db
class TestBookInstanceActions:
    def test_mark_book_as_on_loan(self, book1_available, user1):
        instance = book1_available

        a.mark_book_as_on_loan(instance, user1)

        assert instance.status == 'o'
        assert instance.borrower == user1
        assert instance.due_back > (
            timezone.now() + timezone.timedelta(weeks=2))

    def test_mark_book_as_maintainance(self, book1_available):
        instance = book1_available

        a.mark_book_as_maintainance(instance)

        assert instance.status == 'm'
        assert instance.borrower == None
        assert instance.due_back == None

    def test_mark_book_as_available(self, book1_maintaining):
        instance = book1_maintaining

        a.mark_book_as_available(instance)

        assert instance.status == 'a'
        assert instance.borrower == None
        assert instance.due_back == None
