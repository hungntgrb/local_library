from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("books/", views.BookListView.as_view(), name="books"),
    path("books/available/", views.AvailableBookListView.as_view(), name="avail_books"),
    path("books/<str:pk>/", views.BookDetailView.as_view(), name="book-detail"),
    # ------ CRUD Book ------
    path("books/create/", views.BookCreate.as_view(), name="book_create"),
    path("books/<str:pk>/update/", views.BookUpdate.as_view(), name="book_update"),
    path("books/<str:pk>/delete/", views.BookDelete.as_view(), name="book_delete"),
    path("borrow/<uuid:uid>/", views.borrow_a_book, name="borrow_a_book"),
    path("return/<uuid:uid>/", views.return_a_book, name="return_a_book"),
    # ----------------------------------------------
    path("mybooks/", views.BooksLoanedByUserListView.as_view(), name="my-borrowed"),
    path(
        "borrowed-books/", views.AllBorrowedBooksListView.as_view(), name="all-borrowed"
    ),
    path(
        "book/<uuid:pk>/renew/", views.renew_book_librarian, name="renew-book-librarian"
    ),
    # ----------------- Author ---------------------
    path("authors/", views.AuthorListView.as_view(), name="authors"),
    path("author/<str:pk>", views.AuthorDetailView.as_view(), name="author-detail"),
    # -------- CRUD Author ------------
    path("author/create/", views.AuthorCreate.as_view(), name="author_create"),
    path("author/<str:pk>/update/",
         views.AuthorUpdate.as_view(), name="author_update"),
    path("author/<str:pk>/delete/",
         views.AuthorDelete.as_view(), name="author_delete"),
    # ------- Search ---------
    path("search-result/", views.search_view, name="search_result"),
    path("send-email/", views.send_an_email, name="send_email"),
]
