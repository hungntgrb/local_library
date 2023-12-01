from django.utils import timezone

from catalog.models import BookInstance
from users.models import User


def mark_book_as_on_loan(book: BookInstance,
                         user: User,
                         duration: int = 21):
    book.status = 'o'
    book.due_back = timezone.now() + timezone.timedelta(days=duration)
    book.borrower = user
    book.save()


def mark_book_as_maintainance(book: BookInstance):
    book.status = 'm'
    book.due_back = None
    book.borrower = None
    book.save()


def mark_book_as_available(book: BookInstance):
    book.status = 'a'
    book.due_back = None
    book.borrower = None
    book.save()
