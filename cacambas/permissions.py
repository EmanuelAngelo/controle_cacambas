from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

class IsAuthenticatedAny(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
