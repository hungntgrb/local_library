from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid
from datetime import date


class Genre(models.Model):
    """A Model representing book's genre"""
    name = models.CharField(
        max_length=200, help_text='Enter a book genre. (e.g Science Fiction)')

    def __str__(self):
        """String representing a Genre"""
        return self.name


class Book(models.Model):
    """A class representing a book (not particular copy)."""

    title = models.CharField(max_length=200, help_text='Title of the book.')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000, help_text='Enter a brief description of the book.')
    isbn = models.CharField(
        'ISBN', max_length=13, help_text='<a href="https://en.wikipedia.org/wiki/International_Standard_Book_Number">ISBN Number</a>')
    genre = models.ManyToManyField(
        Genre, help_text='Select genres for this book.')
    language = models.ForeignKey(
        'Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.pk)])

    def display_genre(self):
        """String showing genre of book"""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Model representing a particular copy of book."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for a particular copy of book.')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(blank=True, null=True)
    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True, default='m',
        help_text='Book Availability',
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


class Author(models.Model):
    """Model represent an author"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField('Died', blank=True, null=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        permissions = (
            ('can_crud_author', 'Can create, update, delete author'), )

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Language(models.Model):
    """A model representing languages books are written in."""
    LANGUAGES = (
        ('en', 'English'),
        ('fr', 'French'),
        ('de', 'German'),
        ('es', 'Spanish'),
        ('fa', 'Farsi'),
        ('vi', 'Vietnamese'),
    )
    name = models.CharField(
        max_length=2, choices=LANGUAGES, default='en', blank=True,
        help_text='Select language for this book')

    def __str__(self):
        return self.name
