from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet


class ActivityViewMixin(GenericViewSet):
    no_serializer_actions = []

    def get_serializer_class(self):
        if self.action in self.no_serializer_actions:
            return None
        return self.serializer_class


class LikeViewMixin(ActivityViewMixin):

    def __init__(self, *args, **kwargs):
        self.no_serializer_actions += ['like', 'unlike']
        super().__init__()

    @action(detail=True, methods=['POST'], )
    def like(self, request, pk=None):
        obj = self.get_object()
        obj.is_liked(request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'], )
    def unlike(self, request, pk=None):
        obj = self.get_object()
        obj.is_unliked(request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)


class BookmarkViewMixin(ActivityViewMixin):

    def __init__(self, *args, **kwargs):
        self.no_serializer_actions += ['bookmark', 'unbookmark']
        super().__init__()

    @action(detail=True, methods=['POST'], )
    def bookmark(self, request, pk=None):
        obj = self.get_object()
        obj.is_bookmarked(request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'], )
    def unbookmark(self, request, pk=None):
        obj = self.get_object()
        obj.is_unbookmarked(request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)
