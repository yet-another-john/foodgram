"""Permissions for users."""

from rest_framework import permissions


class IsAuthorOrAdmin(permissions.IsAuthenticatedOrReadOnly):
    """Класс прав доступа."""

    message = 'Недоступно для этого пользователя.'

    def has_object_permission(self, request, view, obj):
        """Проверка прав доступа."""
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
