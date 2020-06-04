from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/available/', views.AvailableBookListView.as_view(), name='avail_books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    # ----------------------------------------------
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    # ----------------------------------------------
    path('mybooks/', views.BooksLoanedByUserListView.as_view(), name='my-borrowed'),
    path('borrowed-books/', views.AllBorrowedBooksListView.as_view(),
         name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian,
         name='renew-book-librarian'),
    # -------- CRUD Author ------------
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/',
         views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/',
         views.AuthorDelete.as_view(), name='author_delete'),
    # ------ CRUD Book ------
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
    path('book/<uuid:uid>/borrow/', views.borrow_a_book, name='borrow_a_book'),
    path('book/<uuid:uid>/return/', views.return_a_book, name='return_a_book'),
    # ------- Search ---------
    path('search-result/', views.search_view, name='search_result'),
    path('send-email/', views.send_an_email, name='send_email'),
]
