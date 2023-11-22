from rest_framework.permissions import BasePermission


class IsLibrarianOrAdmin(BasePermission):
    message = 'Only librarians and admins can do that.'

    def has_permission(self, request, view):
        user = request.user
        allowed = (user.has_perm('catalog.add_book') or
                   user.is_staff)
        return allowed
