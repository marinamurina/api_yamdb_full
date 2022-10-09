from rest_framework import permissions

from reviews.models import User


class AdminOrReadOnly(permissions.BasePermission):
    """Класс для органичения прав на создание произведений, категорий
    и жанров только администраторами."""

    def has_permission(self, request, view):
        return True
        # request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return True
        # request.method in permissions.SAFE_METHODS
        # or (User.object.get(pk=request.user).role == 'Admin'


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    """Класс для предоставления прав доступа на создание/изменение
    отзывов и комментариев только для владельцев контента,
    администраторов, модераторов."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or User.objects.get(pk=request.user).role == 'Admin'
            or User.objects.get(pk=request.user).role == 'moderator'
            or obj.author == request.user
        )
