from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        methods_tuple = ('POST', 'PUT', 'PATCH', 'DELETE',)
        if request.method in methods_tuple and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if(
            request.method == 'DELETE'
            and request.user.is_authenticated
            and (request.user.is_moderator
                 or request.user.is_admin
                 or request.user.is_superuser
                 or obj.author == request.user)

        ):
            return True
        if(
            view.basename == 'title'
            and request.method == 'PATCH'
            and request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)

        ):
            return True
        if (
            (view.basename == 'reviews' or view.basename == 'comments')
            and request.method == 'PATCH' and request.user.is_authenticated
            and request.user.is_moderator or request.user.is_admin
            or request.user.is_superuser or obj.author == request.user
        ):
            return True
        return False


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if (request.method == 'POST'
            or request.method == 'DELETE'
            or request.method == 'PATCH'
            ) and request.user.is_authenticated and (
                request.user.is_admin or request.user.is_superuser):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if (request.method == 'DELETE'
            or request.method == 'PATCH'
            ) and request.user.is_authenticated and (
                request.user.is_moderator or request.user.is_admin
                or request.user.is_superuser):
            return True
        return False


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and (
                request.user.is_admin or request.user.is_superuser):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and (
                request.user.is_admin
                or request.user.is_superuser))


class OnlyOwnAccount(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
