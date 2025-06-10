from django.db import models
from django.utils import timezone


class MyBaseModel(models.Model):
    time_created = models.DateTimeField(auto_now_add=True, blank=True)
    time_updated = models.DateTimeField(auto_now=True, blank=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ("-time_created",)

    @property
    def is_soft_deleted(self) -> bool:
        return self.deleted_at is not None

    def soft_delete(self):
        if self.is_soft_deleted:
            return "No action. Object is already soft-deleted!"
        else:
            self.deleted_at = timezone.now()
            self.save()
            return "Soft-deleted object!"

    def restore(self):
        if not self.is_soft_deleted:
            return "No action. Object is active!"
        else:
            self.deleted_at = None
            self.save()
            return "Restored object!"


# Nguyen Thanh Hung
