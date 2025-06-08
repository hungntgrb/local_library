from django.db import models


class MyBaseModel(models.Model):
    time_created = models.DateTimeField(auto_now_add=True, blank=True)
    time_updated = models.DateTimeField(auto_now=True, blank=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ("-time_created",)


# Nguyen Thanh Hung
