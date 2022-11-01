from django.db import transaction
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from activity.views import LikeViewMixin, BookmarkViewMixin
from .models import Feed, Article
from .serializers import FeedSerializer, ArticleSerializer
from .permissions import IsAdminOrReadOnlyAuthenticated


class FeedViewSet(ModelViewSet):
    queryset = Feed.objects.all().prefetch_related('follows')
    serializer_class = FeedSerializer
    permission_classes = (IsAdminOrReadOnlyAuthenticated, )

    def get_serializer_class(self):
        if self.action in ['follow',]:
            return None
        return super().get_serializer_class()

    @action(detail=True, methods=['POST', ])
    def follow(self, request, pk=None):
        feed = get_object_or_404(self.queryset, pk=pk)
        feed.follow(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArticleViewSet(RetrieveModelMixin,
                     ListModelMixin,
                     LikeViewMixin,
                     BookmarkViewMixin,
                     GenericViewSet):

    queryset = Article.objects.all().annotate(likes_count=Count('likes'))
    serializer_class = ArticleSerializer

    @transaction.atomic
    def retrieve(self, request, pk=None, *args, **kwargs):
        article = get_object_or_404(self.queryset, pk=pk)
        article.is_read(request.user)
        return super().retrieve(request, args, kwargs)

    @action(detail=False, methods=['GET', ])
    def feed(self, request, *args, **kwargs):
        feeds = Feed.objects.get_user_feeds(request.user)
        articles = Article.objects.get_user_feed_items(request.user, feeds)
        serializer = self.get_serializer_class()(articles, many=True)
        return Response(serializer.data)


