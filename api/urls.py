from django.urls import path
from api import views as api_views

urlpatterns = [
    path("books/", api_views.BookList.as_view(), name="book-list"),
    path("books/<int:pk>/", api_views.BookDetail.as_view(), name="book-detail"),
]

