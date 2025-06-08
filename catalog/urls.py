from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("books/", views.BookListView.as_view(), name="books"),
    path("books/available/", views.AvailableBookListView.as_view(), name="avail_books"),
    path("books/<slug:slug>/", views.book_detail, name="book-detail"),
    # ------ CRUD Book ------
    path("add-a-book/", views.BookCreate.as_view(), name="book_create"),
    path("books/<slug:slug>/update/", views.book_update, name="book_update"),
    path("books/<slug:slug>/delete/", views.BookDelete.as_view(), name="book_delete"),
    path("borrow/<uuid:uid>/", views.borrow_a_book, name="borrow_a_book"),
    path("return/<uuid:uid>/", views.return_a_book, name="return_a_book"),
    # ----------------------------------------------
    path("mybooks/", views.BooksLoanedByUserListView.as_view(), name="my-borrowed"),
    path(
        "borrowed-books/", views.AllBorrowedBooksListView.as_view(), name="all-borrowed"
    ),
    path(
        "book/<uuid:uid>/renew/",
        views.renew_book_librarian,
        name="renew-book-librarian",
    ),
    # ----------------- Author ---------------------
    path("authors/", views.AuthorListView.as_view(), name="authors"),
    path("author/<slug:slug>", views.AuthorDetailView.as_view(), name="author-detail"),
    # -------- CRUD Author ------------
    path("author/create/", views.AuthorCreate.as_view(), name="author_create"),
    path(
        "author/<slug:slug>/update/", views.AuthorUpdate.as_view(), name="author_update"
    ),
    path(
        "author/<slug:slug>/delete/", views.AuthorDelete.as_view(), name="author_delete"
    ),
    # ------- Search ---------
    path("search-result/", views.search_view, name="search_result"),
    path("send-email/", views.send_an_email, name="send_email"),
]
