from rest_framework import permissions
from accounts.models import Employee


# Extending from permissions.IsAuthenticated, to make sure we have request.user
class IsCompanyAdmin(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if not is_authenticated:
            return False
        try:
            employee = Employee.objects.get(user=request.user)
            return employee.is_admin == True
        except Employee.DoesNotExist:
            return False
