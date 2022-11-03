from rest_framework.permissions import BasePermission, SAFE_METHODS


class FeedViewPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or view.action in ['follow', 'add', ]:
            return request.user.is_authenticated
        else:
            return request.user.is_superuser
