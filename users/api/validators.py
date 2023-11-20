from django.conf import settings
from rest_framework.validators import ValidationError


def password_long_enough(password):
    min_length = settings.PASSWORD_MIN_LENGTH

    if len(password) < min_length:
        raise ValidationError(
            f'Too short! Password must be at least {min_length} characters long.')
    return password
