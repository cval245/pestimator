from rest_framework import permissions


class DataPermission(permissions.BasePermission):
    message = 'access to template data forbidden'

    def has_permission(selfself, request, view):
        if request.user.admin_data:
            return True
        else:
            return False


class PostFamFormPermission(permissions.BasePermission):
    message = 'Please purchase additional estimates'

    def has_permission(self, request, view):
        if view.action == 'create' or view.action == 'update' or view.action == 'partial_update':
            if request.user.userprofile.estimates_remaining > 0:
                return True
            else:
                return False
        else:
            return True
