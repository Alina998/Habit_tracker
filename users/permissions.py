from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    message = "Доступ запрещен"

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False


class IsOwner(BasePermission):
    message = "Доступ запрещен"

    def has_object_permission(self, request, view, obj):
        if request.user == obj or request.user.is_staff:
            return True
        return False
