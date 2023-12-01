from typing import Any
from django.db import models
from secrets import token_hex
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser, UserManager


def hex_token_20():
    return token_hex(10)


class MyUserManager(UserManager):
    def create_staff(self, username: str,
                     email: str | None = ...,
                     password: str | None = ...):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    id = models.CharField(
        primary_key=True, max_length=25, blank=True, default=hex_token_20
    )
    email = models.EmailField(
        _('Email'), max_length=150, unique=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()
