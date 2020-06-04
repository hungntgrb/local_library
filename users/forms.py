from django import forms


class EmailForm(forms.Form):
    email_address = forms.EmailField(
        help_text='Registraion link will be sent to this email.')
