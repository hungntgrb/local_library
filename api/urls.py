from django.urls import path
from api import views as api_views


app_name = "api"


urlpatterns = [
    path("books/", api_views.book_list, name="book_list"),
    path("add-new-book/", api_views.book_create, name="book_create"),
    path("book/<str:pk>/", api_views.book_retrieve, name="book_retrieve"),
    # path("update-book/<str:pk>/", api_views.book_update, name="book_update"),
    # path("remove-book/<str:pk>/", api_views.book_destroy, name="book_destroy"),
    # --- Authors ---
    path("authors/", api_views.author_list, name="author_list"),
    path("authors/<str:pk>/", api_views.author_retrieve, name="author_retrieve"),
    # path("add-an-author/<str:pk>/", api_views.author_create, name="author_create"),
    # path("update-author/<str:pk>/", api_views.author_update, name="author_update"),
    # path("delete-author/<str:pk>/",
    #      api_views.author_destroy, name="author_destroy"),
]
