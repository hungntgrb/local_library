from django.db import models
from secrets import token_hex


def hex_token_20():
    return token_hex(10)


class MyBaseModel(models.Model):
    id = models.CharField(
        primary_key=True, max_length=20, blank=True, default=hex_token_20
    )
    time_created = models.DateTimeField(
        auto_now_add=True, blank=True
    )
    time_updated = models.DateTimeField(
        auto_now=True, blank=True
    )

    class Meta:
        abstract = True
        ordering = ('-time_created',)
