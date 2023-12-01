import uuid
from datetime import date
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from locallibrary.models import MyBaseModel


class Genre(MyBaseModel):
    """A Model representing Book's Genre"""
    name = models.CharField(
        max_length=200,
        help_text=_('Enter a book genre. (e.g Science Fiction)')
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """String representing a Genre"""
        return self.name


class Book(MyBaseModel):
    """A class representing a Book (not particular copy)."""

    title = models.CharField(
        max_length=200,
        help_text=_('Title of the book.'),
        blank=False,
        null=False
    )
    author = models.ForeignKey(
        'Author',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    summary = models.TextField(
        max_length=1000,
        help_text=_('Enter a brief description of the book.'),
        blank=True,
        null=True
    )
    isbn = models.CharField(
        _('ISBN'),
        max_length=13,
        help_text='<a href="https://en.wikipedia.org/wiki/International_Standard_Book_Number">ISBN Number</a>',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        help_text=_('Select genres for this book.'),
        blank=True,
        null=True
    )
    language = models.ForeignKey(
        'Language',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.pk)])

    def display_genre(self):
        """String showing genre of book"""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = 'Genre'


class BookInstance(MyBaseModel):
    """Model representing a particular copy of Book."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text=_('Unique ID for a particular copy of book.')
    )
    book = models.ForeignKey(
        'Book',
        on_delete=models.SET_NULL,
        null=True
    )
    imprint = models.CharField(
        max_length=200,
        blank=True,
        default='Some Imprint X'
    )
    due_back = models.DateField(
        blank=True,
        null=True
    )
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text=_('Book Availability'),
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set books as return"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        if self.due_back and (date.today() > self.due_back):
            return True
        return False

    def days_left(self):
        return (self.due_back - date.today()).days

    @property
    def is_on_loan(self):
        return (self.status == 'o' and
                self.borrower is not None)

    @property
    def is_available(self):
        return (self.status == 'a' and
                self.borrower is None)


class Author(MyBaseModel):
    """Model represent an Author"""
    first_name = models.CharField(
        max_length=100
    )
    last_name = models.CharField(
        max_length=100
    )
    date_of_birth = models.DateField(
        _('Born'),
        blank=True,
        null=True
    )
    date_of_death = models.DateField(
        _('Died'),
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('last_name', 'first_name')
        permissions = (
            ('can_crud_author', 'Can create, retrieve, update, delete author'),
        )

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.id})

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Language(MyBaseModel):
    """A model representing Languages in which Books are written."""
    LANGUAGES = (
        ('en', 'English'),
        ('fr', 'French'),
        ('de', 'German'),
        ('es', 'Spanish'),
        ('fa', 'Farsi'),
        ('vi', 'Vietnamese'),
        ('kr', 'Korean'),
        ('jp', 'Japanese'),
    )
    name = models.CharField(
        max_length=2,
        choices=LANGUAGES,
        default='en',
        blank=True,
        help_text=_('Select language for this book')
    )

    def __str__(self):
        return self.name
