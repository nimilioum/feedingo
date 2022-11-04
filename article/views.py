from django.db import transaction, IntegrityError
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from activity.views import LikeViewMixin, BookmarkViewMixin
from utils.exception import FeedFetchFailedException
from rss.services import RSSParser
from .models import Feed, Article
from .serializers import FeedSerializer, ArticleSerializer, FeedAddSerializer
from .permissions import FeedViewPermission


class FeedViewSet(ModelViewSet):
    queryset = Feed.objects.all().annotate(follows_count=Count('follows'))
    serializer_class = FeedSerializer
    permission_classes = (FeedViewPermission,)

    def get_serializer_class(self):
        if self.action in ['follow', ]:
            return None

        if self.action == 'add':
            return FeedAddSerializer

        return super().get_serializer_class()

    @action(detail=True, methods=['POST', ])
    def follow(self, request, pk=None):
        feed = get_object_or_404(self.queryset, pk=pk)
        try:
            feed.follow(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except IntegrityError:
            return Response(data={'msg': 'feed is already followed'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET', ])
    def followed(self, request):
        queryset = Feed.objects.user_followed(request.user).annotate(follows_count=Count('follows'))
        serializer = FeedSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST', ], serializer_class=FeedSerializer)
    @swagger_auto_schema(responses={200: FeedSerializer()})
    def add(self, request):
        serializer = FeedAddSerializer(data=request.data)
        if serializer.is_valid():
            link = serializer.validated_data['url']
            try:
                parser = RSSParser(link)
                feed = parser.get_feed()
                articles = parser.get_articles()

                feed.save()

                feed.add_articles(articles)
                Article.objects.bulk_create(articles)
                feed.article_set.set(articles)

                return Response(FeedAddSerializer(feed).data)

            except IntegrityError:    # for duplicate rss link
                feed = Feed.objects.get(rss_url=link)
                feed.follow(request.user)
                return Response(FeedAddSerializer(feed).data)

            except FeedFetchFailedException as e:
                return Response({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"msg": f'{serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)


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
        feeds = Feed.objects.get_user_feed_ids(request.user)
        articles = Article.objects.get_user_feed_items(request.user, feeds)
        serializer = self.get_serializer_class()(articles, many=True)
        return Response(serializer.data)


