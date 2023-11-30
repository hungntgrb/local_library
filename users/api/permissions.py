from rest_framework.permissions import BasePermission


class GuestOnly(BasePermission):
    message = 'User already logged-in.'

    def has_permission(self, request, view):
        user = request.user
        return (not user.is_authenticated)
