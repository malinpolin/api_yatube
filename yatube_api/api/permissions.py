from rest_framework import permissions

METHODS_FOR_AUTH_USER = ('GET', 'POST')
METHODS_FOR_AUTHOR = ('PATCH', 'PUT', 'DELETE')


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in METHODS_FOR_AUTHOR:
            return obj.author == request.user
        if request.method in METHODS_FOR_AUTH_USER:
            return True
        return False
