from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class EmailForm(forms.Form):
    email_address = forms.EmailField(
        help_text='Registration link will be sent to this email.')


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username')
