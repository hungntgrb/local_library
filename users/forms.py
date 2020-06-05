from django import forms


class EmailForm(forms.Form):
    email_address = forms.EmailField(
        help_text='Registration link will be sent to this email.')
