import uuid
import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User, Permission


from catalog.models import Author, Book, BookInstance, Genre, Language


class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_authors = 5
        for author in range(number_of_authors):
            Author.objects.create(first_name=f'Peter {author}',
                                  last_name=f'Parker {author}')

    def test_url_is_accessible(self):
        res = self.client.get('/catalog/authors/')
        self.assertEqual(res.status_code, 200)

    def test_url_can_be_derive_by_name(self):
        res = self.client.get(reverse('authors'))
        self.assertEqual(res.status_code, 200)

    def test_view_use_the_correct_template(self):
        res = self.client.get(reverse('authors'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'catalog/author_list.html')

    def test_pagination_is_three(self):
        res = self.client.get(reverse('authors'))
        self.assertEqual(res.status_code, 200)
        self.assertTrue('is_paginated' in res.context)
        self.assertTrue(res.context['is_paginated'] == True)
        self.assertTrue(len(res.context['author_list']) == 3)

    def test_all_authors_are_displayed(self):
        res = self.client.get(reverse('authors') + '?page=2')
        self.assertEqual(res.status_code, 200)
        self.assertTrue('is_paginated' in res.context)
        self.assertTrue(res.context['is_paginated'] == True)
        self.assertTrue(len(res.context['author_list']) == 2)


class LoanedBookInstanceByUserListViewTest(TestCase):
    def setUp(self):
        # create 2 users
        test_user1 = User.objects.create_user(
            username='testuser1', password='Xjaoemgn172fh')
        test_user2 = User.objects.create_user(
            username='testuser2', password='lIIfmeYkwkl82')
        test_user1.save()
        test_user2.save()

        # create a book
        test_author = Author.objects.create(
            first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='en')
        test_book = Book.objects.create(
            title='My Test Book',
            summary='My book\'s summary',
            isbn='123ABCGHTH',
            author=test_author,
            language=test_language,
        )
        genre_for_book = Genre.objects.all()
        # Direct assignment not allowed for Many-To-Many
        test_book.genre.set(genre_for_book)
        test_book.save()

        # create 30 book instances
        num_of_book_copies = 30
        for book_copy in range(num_of_book_copies):
            return_date = timezone.localtime() + timezone.timedelta(days=book_copy % 5)
            the_borrower = test_user1 if book_copy % 2 else test_user2
            imprint = 'Gi cung duoc, 2018'
            status = 'm'
            BookInstance.objects.create(
                book=test_book,
                imprint=imprint,
                due_back=return_date,
                borrower=the_borrower,
                status=status,
            )

    def test_redirect_if_not_logged_in(self):
        res = self.client.get(reverse('my-borrowed'))
        self.assertRedirects(res, '/accounts/login/?next=/catalog/mybooks/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(
            username='testuser1', password='Xjaoemgn172fh')
        res = self.client.get(reverse('my-borrowed'))
        self.assertTrue(str(res.context['user']) == 'testuser1')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'catalog/books_loaned_by_user.html')

    def test_only_borrowed_books_displayed(self):
        login = self.client.login(
            username='testuser1', password='Xjaoemgn172fh')
        res = self.client.get(reverse('my-borrowed'))

        self.assertTrue(str(res.context['user']) == 'testuser1')
        self.assertEqual(res.status_code, 200)
        self.assertTrue('bookinstance_list' in res.context)
        self.assertEqual(len(res.context['bookinstance_list']), 0)

        books = BookInstance.objects.all()[:10]
        for book in books:
            book.status = 'o'
            book.save()

        res = self.client.get(reverse('my-borrowed'))
        self.assertTrue(str(res.context['user']) == 'testuser1')
        self.assertEqual(res.status_code, 200)
        self.assertTrue('bookinstance_list' in res.context)

        for bookitem in res.context['bookinstance_list']:
            self.assertEqual(res.context['user'], bookitem.borrower)
            self.assertEqual('o', bookitem.status)

    def test_borrowed_books_ordered_by_due_date(self):
        # Change all books to Onloan
        books = BookInstance.objects.all()
        for book in books:
            book.status = 'o'
            book.save()

        login = self.client.login(
            username='testuser1', password='Xjaoemgn172fh')
        res = self.client.get(reverse('my-borrowed'))

        self.assertTrue(str(res.context['user']) == 'testuser1')
        self.assertEqual(res.status_code, 200)
        self.assertTrue('bookinstance_list' in res.context)
        self.assertEqual(len(res.context['bookinstance_list']), 10)

        last_date = 0
        for bookitem in res.context['bookinstance_list']:
            if last_date == 0:
                last_date = bookitem.due_back
            else:
                self.assertTrue(last_date <= bookitem.due_back)
                last_date = bookitem.due_back


class RenewBookInstancesViewTest(TestCase):
    def setUp(self):

        # create 2 users
        test_user1 = User.objects.create_user(
            username='testuser1', password='20026069c85470962')
        test_user2 = User.objects.create_user(
            username='testuser2', password='b07d8dcfce150246e')
        test_user1.save()
        test_user2.save()

        my_permission = Permission.objects.get(name='Set books as return')
        test_user2.user_permissions.add(my_permission)
        test_user2.save()

        # Create a book
        test_author = Author.objects.create(
            first_name='Bruce', last_name='Banner')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='en')
        test_book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            isbn='AQWERTGFD',
            author=test_author,
            language=test_language,
        )
        # Add Genre later, direct assignment not allowed for Many-To-Many
        genres = Genre.objects.all()
        test_book.genre.set(genres)
        test_book.save()

        # Create 2 book instances
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance1 = BookInstance.objects.create(
            book=test_book,
            imprint='Some Imprint, 2020',
            borrower=test_user1,
            due_back=return_date,
            status='o'
        )
        self.test_bookinstance2 = BookInstance.objects.create(
            book=test_book,
            imprint='Some Imprint, 2020',
            borrower=test_user2,
            due_back=return_date,
            status='o'
        )
        self.renew_url_valid_book = reverse(
            'renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk})

    def test_redirect_if_not_logged_in(self):
        res = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(res.status_code, 302)
        self.assertTrue(res.url.startswith('/accounts/login/'))

    def test_redirect_if_logged_in_but_not_have_perm(self):
        login = self.client.login(
            username='testuser1', password='20026069c85470962')
        res = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        # Please Login with an account that has access.
        self.assertEqual(res.status_code, 302)

    def test_logged_in_with_perm_borrowed_book(self):
        login = self.client.login(
            username='testuser2', password='b07d8dcfce150246e')
        res = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance2.pk}))
        self.assertEqual(res.status_code, 200)

    def test_logged_in_with_perm_other_users_book(self):
        login = self.client.login(
            username='testuser2', password='b07d8dcfce150246e')
        res = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance2.pk}))
        self.assertEqual(res.status_code, 200)

    def test_HTTP404_invalid_book(self):
        test_uid = uuid.uuid4()
        login = self.client.login(
            username='testuser2', password='b07d8dcfce150246e')
        res = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': test_uid}))
        self.assertEqual(res.status_code, 404)

    def test_logged_in_correct_template(self):
        login = self.client.login(
            username='testuser2', password='b07d8dcfce150246e')
        res = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance2.pk}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'catalog/book_renew_librarian.html')

    def test_renew_form_initially_date_three_weeks_in_future(self):
        login = self.client.login(
            username='testuser2', password='b07d8dcfce150246e')
        res = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(res.status_code, 200)

        three_weeks_in_future = datetime.date.today() + datetime.timedelta(weeks=3)
        self.assertEqual(
            res.context['form'].initial['due_back'], three_weeks_in_future)

    def test_redirect_renew_success(self):
        login = self.client.login(
            username='testuser2', password='b07d8dcfce150246e')
        valid_renewal_date = datetime.date.today() + datetime.timedelta(weeks=2)
        res = self.client.post(
            reverse('renew-book-librarian',
                    kwargs={'pk': self.test_bookinstance1.pk}),
            {'due_back': valid_renewal_date},
            follow=True)
        self.assertRedirects(res, reverse('all-borrowed'))

    def test_form_invalid_date_in_past(self):
        date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)
        login = self.client.login(
            username='testuser2', password='b07d8dcfce150246e')
        res = self.client.post(self.renew_url_valid_book,
                               {'due_back': date_in_past})
        self.assertEqual(res.status_code, 200)
        self.assertFormError(res, 'form', 'due_back',
                             'Invalid date - Renewal đã qua')

    def test_form_invalid_date_in_future(self):
        invalid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=5)
        login = self.client.login(
            username='testuser2', password='b07d8dcfce150246e')
        res = self.client.post(self.renew_url_valid_book,
                               {'due_back': invalid_date_in_future})
        self.assertEqual(res.status_code, 200)
        self.assertFormError(res, 'form', 'due_back',
                             'Invalid date - Renewal more than 4 weeks ahead')
