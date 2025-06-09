from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "books/",
        include(
            [
                path("", views.book_list, name="books"),
                path("available/", views.available_book_list, name="avail_books"),
                path("add-new/", views.book_create, name="book_create"),
                path(
                    "my-borrows/",
                    views.BooksLoanedByUserListView.as_view(),
                    name="my-borrowed",
                ),
            ]
        ),
    ),
    path(
        "books/<slug:slug>/",
        include(
            [
                path("", views.book_detail, name="book-detail"),
                path("update/", views.book_update, name="book_update"),
                path("delete/", views.book_delete, name="book_delete"),
            ]
        ),
    ),
    path(
        "copies/",
        include(
            [
                path("all-borrowed/", views.all_borrowed_copies, name="all-borrowed"),
                path("<uuid:uid>/borrow/", views.borrow_a_book, name="borrow_a_book"),
                path("<uuid:uid>/return/", views.return_a_book, name="return_a_book"),
                path(
                    "<uuid:uid>/renew/",
                    views.renew_book_librarian,
                    name="renew-book-librarian",
                ),
            ]
        ),
    ),
    # ----------------- Author ---------------------
    path("authors/", views.author_list, name="authors"),
    path("authors/create/", views.author_create, name="author_create"),
    path(
        "authors/<slug:slug>/",
        include(
            [
                path("", views.author_detail, name="author-detail"),
                path("update/", views.author_update, name="author_update"),
                path("delete/", views.author_delete, name="author_delete"),
            ]
        ),
    ),
    # ------- Search ---------
    path("search-result/", views.search_view, name="search_result"),
    path("send-email/", views.send_an_email, name="send_email"),
]
