import datetime
import os

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail

from .models import Book, Author, BookInstance, Genre
from .forms import RenewBookForm, RenewBookModelForm


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()

    # Get the visit count from session
    # del request.session['num_visits']
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_genres": num_genres,
        "num_visits": num_visits,
    }
    return render(request, "index.html", context=context)


class BookListView(generic.ListView):
    queryset = Book.objects.all().order_by("title")
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books_count"] = Book.objects.count()
        return context


class AvailableBookListView(generic.ListView):
    queryset = BookInstance.objects.filter(status="a").order_by("book")
    template_name = "catalog/available_books.html"


def borrow_a_book(request, uid):
    book_copy = BookInstance.objects.get(pk=uid)

    currently_borrowing_books = map(
        lambda x: x.book, request.user.bookinstance_set.all()
    )
    # Only borrow 1 copy of a book at one time
    if book_copy.book in currently_borrowing_books:
        messages.error(
            request,
            f'You are currently borrowing a copy of <a class="alert-link">{book_copy.book}</a>.',
            extra_tags="safe",
        )
        return redirect(reverse("avail_books"))
    elif request.user.bookinstance_set.count() >= 3:
        my_books = reverse("my-borrowed")
        messages.error(
            request,
            f'You cannot have more than 3 copies at a time. <a href="{my_books}" class="alert-link">Return one</a> so that you can borrow another.',
            extra_tags="safe",
        )
        return redirect(reverse("avail_books"))
    else:
        book_copy.status = "o"
        book_copy.borrower = request.user
        book_copy.due_back = datetime.date.today() + datetime.timedelta(weeks=3)
        book_copy.save()
        # Display message
        on_shelf = reverse("avail_books")
        messages.success(
            request,
            f'You have successfully borrowed <a class="alert-link">{book_copy.book}</a>. <br/><a class="alert-link" href="{on_shelf}">Borrow another one?</a>',
            extra_tags="safe",
        )
        return redirect(reverse("my-borrowed"))


def return_a_book(request, uid):
    book_copy = BookInstance.objects.filter(pk=uid)
    changes = {"status": "a", "borrower": None, "due_back": None}
    book_copy.update(**changes)

    book_name = book_copy.first().book.title

    messages.success(
        request,
        f'You have returned <a class="alert-link">{book_name}</a>.',
        extra_tags="safe",
    )

    return redirect(reverse("my-borrowed"))


class BooksLoanedByUserListView(LoginRequiredMixin, generic.ListView):
    """A list view of books that are on loan by current user"""

    # model = BookInstance
    paginate_by = 10
    template_name = "catalog/my-books.html"

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact="o")
            .order_by("due_back")
        )


class AllBorrowedBooksListView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.ListView
):
    """A view available for Librarians to see all borrowed books"""

    model = BookInstance

    paginate_by = 10
    template_name = "catalog/all_borrowed_books.html"
    permission_required = "catalog.can_mark_returned"

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact="o").order_by("due_back")


class BookDetailView(generic.DetailView):
    model = Book
    redirect_field_name = "chuyen_toi"


class AuthorListView(generic.ListView):
    queryset = Author.objects.all().order_by("first_name")
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_of_authors"] = Author.objects.count()
        return context


class AuthorDetailView(generic.DetailView):
    model = Author


@permission_required("catalog.can_mark_returned")
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == "POST":
        form = RenewBookModelForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data["due_back"]
            book_instance.save()

            return HttpResponseRedirect(reverse("all-borrowed"))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={"due_back": proposed_renewal_date})

    context = {"form": form, "book_instance": book_instance}

    return render(request, "catalog/book_renew_librarian.html", context)


# --------- CREATE, UPDATE, DELETE AUTHOR ----------------


class AuthorCreate(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Author
    fields = "__all__"
    initial = {"date_of_death": "01/01/2020"}
    permission_required = "catalog.add_author"
    success_message = f"Author created successfully!"


class AuthorUpdate(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Author
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]
    permission_required = "catalog.change_author"
    success_message = f"<%(first_name)s %(last_name)s> has been successfully updated!"


class AuthorDelete(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Author
    permission_required = "catalog.delete_author"
    success_url = reverse_lazy("authors")
    success_message = f"Author deleted!"


# ------------ ADD, REMOVE, CHANGE BOOKS ------------ #


class BookCreate(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Book
    fields = ["title", "author", "summary", "isbn", "genre", "language"]
    permission_required = "catalog.add_book"
    success_message = f"Book successfully created!"


class BookUpdate(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Book
    fields = "__all__"
    permission_required = "catalog.change_book"
    success_message = f"Book successfully updated!"


class BookDelete(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Book
    permission_required = "catalog.delete_book"
    success_url = reverse_lazy("books")
    success_message = f"Book successfully deleted!"


def search_view(request):
    q = request.GET.get("q")
    book_results = Book.objects.filter(Q(title__icontains=q) | Q(summary__icontains=q))
    author_results = Author.objects.filter(
        Q(first_name__icontains=q) | Q(last_name__icontains=q)
    )
    context = {
        "books": book_results,
        "authors": author_results,
    }
    return render(request, "catalog/search_result.html", context)


def send_an_email(request):
    send_mail(
        "Hello from Django!",
        "A very interesing body.",
        os.environ.get("EMAIL_USER1"),
        ["hungnt89@gmail.com",],
        fail_silently=False,
        html_message="<h1>Test HTML</h1>",
    )
    messages.success(request, "Email sent!")
    return redirect(reverse("index"))

