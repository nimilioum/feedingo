from rest_framework.serializers import Serializer, ModelSerializer, IntegerField
from .models import Feed, Article


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

    likes = IntegerField(source='likes_count', read_only=True)


class FeedSerializer(ModelSerializer):
    class Meta:
        model = Feed
        fields = '__all__'

    follows = IntegerField(source='follows.count', read_only=True)
    articles = ArticleSerializer(many=True, read_only=True, source='article_set')
