from django.urls import path

from . import views as api


app_name = 'users_api'

urlpatterns = [
    path('register/', api.user_create, name='user_create'),
    path('', api.user_list, name='user_list'),
    path('login/', api.user_login, name='login'),
    # path('logout/', api.user_list, name='logout'),
]
