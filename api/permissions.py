from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = "You dont have permission to access to this api"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == "admin"


class IsModerator(permissions.BasePermission):
    message = "You dont have permission to access to this api"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == "moderator"


class IsAdminOrModerator(permissions.BasePermission):
    message = "You dont have permission to access to this api"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role in ["admin", "moderator"]
