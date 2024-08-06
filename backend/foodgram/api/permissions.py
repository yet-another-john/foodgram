from rest_framework import permissions
from rest_framework.permissions import BasePermission


class RecipePermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
        ) or obj.author == request.user

    def has_permission(self, request, view):
        return not request.user.is_anonymous or (
            request.method in permissions.SAFE_METHODS
        )
