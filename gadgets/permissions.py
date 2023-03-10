from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class ReadOnlyForAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if not is_authenticated:
            return False
        return request.method in SAFE_METHODS
