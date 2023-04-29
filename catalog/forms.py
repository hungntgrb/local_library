import datetime

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import BookInstance


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Enter a date between now and 4 weeks (default 3 weeks)."
    )

    def clean_renewal_date(self):
        data = self.cleaned_data.get("renewal_date")
        today = datetime.date.today()
        gt4w = datetime.timedelta(weeks=4)

        if data < today:
            raise ValidationError(_("Invalid date - Renewal in the past"))
        elif data > today + gt4w:
            raise ValidationError(
                _("Invalid date - Renewal more than 4 weeks ahead"))

        return data


class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data.get("due_back")
        today = datetime.date.today()
        if data < today:
            raise ValidationError(_("Invalid date - Renewal đã qua"))
        elif data > today + datetime.timedelta(weeks=4):
            raise ValidationError(
                _("Invalid date - Renewal more than 4 weeks ahead"))
        return data

    class Meta:
        model = BookInstance
        fields = ("due_back",)
        labels = {"due_back": _("Renewal Date")}
        help_texts = {
            "due_back": _("Enter a date between today and 4 weeks (default 3 weeks).")
        }
