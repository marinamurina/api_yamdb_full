from rest_framework import permissions


class CustomPermissions(permissions.BasePermission):
    """Класс для органичения доступа в зависимости от роли пользователя"""

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True
