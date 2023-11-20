from django.conf import settings
from rest_framework import serializers as s

from users.models import User
from . import validators as v


class UserCreateSerializer(s.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
        read_only_fields = ('id',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def validate_password(self, password):
        return v.password_long_enough(password)


class UserSerializer(s.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name', 'is_staff')


class UserLoginSerializer(s.Serializer):

    username = s.CharField(read_only=True)
    email = s.EmailField(required=True)
    password = s.CharField(required=True, write_only=True)

    def validate_password(self, password):
        pw = v.password_long_enough(password)
        return pw


# from users.api.serializers import *
