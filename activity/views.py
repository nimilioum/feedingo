# from django.core.exceptions import
from django.db.utils import IntegrityError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from .models import Like, Bookmark


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
        try:
            obj = self.get_object()
            obj.is_liked(request.user)

            return Response(status=status.HTTP_204_NO_CONTENT)
        except IntegrityError as e:
            return Response(data={'msg': 'article is already liked'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'], )
    def unlike(self, request, pk=None):
        try:
            obj = self.get_object()
            obj.is_unliked(request.user)

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response(data={'msg': 'article is not liked'},
                            status=status.HTTP_400_BAD_REQUEST)


class BookmarkViewMixin(ActivityViewMixin):

    def __init__(self, *args, **kwargs):
        self.no_serializer_actions += ['bookmark', 'unbookmark']
        super().__init__()

    @action(detail=True, methods=['POST'], )
    def bookmark(self, request, pk=None):
        try:
            obj = self.get_object()
            obj.is_bookmarked(request.user)

            return Response(status=status.HTTP_204_NO_CONTENT)
        except IntegrityError:
            return Response(data={'msg': 'article is already bookmarked'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'], )
    def unbookmark(self, request, pk=None):
        try:
            obj = self.get_object()
            obj.is_unbookmarked(request.user)

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Bookmark.DoesNotExist:
            return Response(data={'msg': 'article is not bookmarked'},
                            status=status.HTTP_400_BAD_REQUEST)
