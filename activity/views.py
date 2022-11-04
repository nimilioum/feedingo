from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from .serializers import CommentSerializer


class LikeViewMixin(GenericViewSet):

    @action(detail=True, methods=['POST'], serializer_class=None)
    def like(self, request, pk=None):
        obj = self.get_object()
        obj.like(request.user)

        return Response(status=status.HTTP_201_CREATED)

    @like.mapping.delete
    def unlike(self, request, pk=None):
        obj = self.get_object()
        obj.unlike(request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)


class BookmarkViewMixin(GenericViewSet):

    @action(detail=True, methods=['POST'], serializer_class=None)
    def bookmark(self, request, pk=None):
        obj = self.get_object()
        obj.bookmark(request.user)

        return Response(status=status.HTTP_201_CREATED)

    @bookmark.mapping.delete
    def unbookmark(self, request, pk=None):
        obj = self.get_object()
        obj.unbookmark(request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewMixin(GenericViewSet):

    @action(detail=True, methods=['POST'], serializer_class=CommentSerializer, url_path='comment')
    def add_comment(self, request, pk=None):
        obj = self.get_object()
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.validated_data['message']
        obj.add_comment(request.user, message)

        return Response(status=status.HTTP_201_CREATED)
