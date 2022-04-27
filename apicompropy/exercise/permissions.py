from rest_framework.permissions import BasePermission, SAFE_METHODS


class HasExercisePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'PUT':
            return request.user == obj.author
        if request.method == 'DELETE':
            return bool(request.user == obj.author or request.user and request.user.is_staff)


class IsUserOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'PUT':
            return request.user == obj
        if request.method == 'DELETE':
            return bool(request.user == obj or request.user and request.user.is_staff)


class AllowUnauthorised(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' and view.action == 'register':
            return bool(not request.user or not request.user.is_authenticated)
        else:
            return True


class IsSubscriberOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        self_subscribe = bool(request.user.pk == request.data.get('followed'))
        return bool(request.user.is_authenticated and not self_subscribe)

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return obj.subscriber == request.user


class AllowReceiverOnlyToDelete(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE', 'PUT']:
            return obj.receiver == request.user


class AuthenticatedOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj