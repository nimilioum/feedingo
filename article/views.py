from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from activity.views import LikeViewMixin, BookmarkViewMixin, CommentViewMixin
from rss.services import RSSParser
from .models import Feed, Article
from .serializers import FeedSerializer, ArticleSerializer, FeedAddSerializer, FeedDetailSerializer
from .permissions import FeedViewPermission


class FeedViewSet(ModelViewSet):
    queryset = Feed.objects.all().annotate(follows_count=Count('follows')).prefetch_related('article_set')
    serializer_class = FeedSerializer
    permission_classes = (FeedViewPermission,)

    def get_serializer_class(self):
        if self.action in ['follow', 'unfollow']:
            return None

        if self.action == 'add':
            return FeedAddSerializer

        if self.action == 'retrieve':
            return FeedDetailSerializer

        return super().get_serializer_class()

    def get_serializer_context(self):
        return {'user': self.request.user}

    @action(detail=True, methods=['POST', ])
    def follow(self, request, pk=None):
        feed = get_object_or_404(self.queryset, pk=pk)
        feed.follow(request.user)
        return Response(status=status.HTTP_201_CREATED)

    @follow.mapping.delete
    def unfollow(self, request, pk=None):
        feed = get_object_or_404(self.queryset, pk=pk)
        feed.unfollow(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET', ])
    def followed(self, request):
        queryset = Feed.objects.user_followed(request.user).annotate(follows_count=Count('follows'))
        serializer = FeedSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST', ], serializer_class=FeedSerializer)
    def add(self, request):
        serializer = FeedAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        link = serializer.validated_data['url']
        feed = Feed.objects.filter(rss_url=link).first()

        if feed is None:
            parser = RSSParser(link)
            feed = parser.get_feed()
            articles = parser.get_articles()

            feed.save()
            feed.add_articles(articles)
            Article.objects.bulk_create(articles)

            feed.article_set.set(articles)

        feed.follow(request.user)
        return Response(FeedAddSerializer(feed).data, status=status.HTTP_201_CREATED)


class ArticleViewSet(RetrieveModelMixin,
                     ListModelMixin,
                     LikeViewMixin,
                     BookmarkViewMixin,
                     CommentViewMixin,
                     GenericViewSet):

    queryset = Article.objects.all().annotate(likes_count=Count('likes')).prefetch_related('comments')
    serializer_class = ArticleSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        article = get_object_or_404(self.queryset, pk=pk)
        article.read(request.user)
        return super().retrieve(request, args, kwargs)

    @action(detail=False, methods=['GET', ])
    def feed(self, request, *args, **kwargs):
        feeds = Feed.objects.get_user_feed_ids(request.user)
        articles = Article.objects.get_user_feed_items(request.user, feeds)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


