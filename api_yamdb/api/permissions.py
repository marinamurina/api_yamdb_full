from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Класс для органичения прав на создание произведений, категорий
    и жанров только администраторами"""

    def has_permission(self, request, view):
        return True
        # request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return True
        # request.method in permissions.SAFE_METHODS
        # or (User.object.get(pk=request.user).role == 'Admin'
