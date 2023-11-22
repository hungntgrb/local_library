from django.urls import path
from api import views as api_views


app_name = "api"


urlpatterns = [
    path("books/", api_views.book_list, name="book_list"),
    path("books/_add/", api_views.book_create, name="book_create"),
    path("books/<str:pk>/", api_views.book_rud, name="book_detail"),
]
