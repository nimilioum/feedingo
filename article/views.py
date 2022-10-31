from rest_framework.viewsets import ModelViewSet
from .models import Feed, Article
from .serializers import FeedSerializer, ArticleSerializer


class FeedViewSet(ModelViewSet):
    queryset = Feed.objects.all().prefetch_related('follows')
    serializer_class = FeedSerializer
