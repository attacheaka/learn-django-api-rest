from rest_framework.permissions import BasePermission, SAFE_METHODS


# Add Author permission
class IsOwner(BasePermission):
    message = 'Editing posts is restricted to the author only.'
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user