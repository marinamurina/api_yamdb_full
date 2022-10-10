from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Класс для органичения прав на создание произведений, категорий
    и жанров только администраторами."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_admin
            )
        else:
            return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_admin
            )
        else:
            return request.method in permissions.SAFE_METHODS


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    """Класс для предоставления прав доступа на изменение
    отзывов и комментариев для владельцев контента,
    администраторов, модераторов."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):

        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
