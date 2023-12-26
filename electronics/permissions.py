from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken


def get_user_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


class IsActiveEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        """
          Пользователь должен быть активным сотрудником.
          """
        return request.user.is_authenticated and request.user.is_active


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Пользователь может редактировать или удалять свои объекты, но может только просматривать чужие.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Проверяем, является ли пользователь владельцем объекта
        return obj.created_at == request.user.created_at