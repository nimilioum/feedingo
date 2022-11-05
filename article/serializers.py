from rest_framework.serializers import Serializer, ModelSerializer, IntegerField, \
    URLField, SerializerMethodField
from activity.serializers import CommentSerializer
from .models import Feed, Article


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

    likes = IntegerField(source='likes_count', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)


class FeedSerializer(ModelSerializer):
    class Meta:
        model = Feed
        fields = '__all__'

    follows = IntegerField(source='follows_count', read_only=True)


class FeedDetailSerializer(ModelSerializer):
    class Meta:
        model = Feed
        fields = '__all__'

    follows = IntegerField(source='follows_count', read_only=True)
    is_followed = SerializerMethodField(read_only=True, source='is_followed')
    articles = ArticleSerializer(many=True, read_only=True, source='article_set')

    def get_is_followed(self, obj):
        return obj.is_followed(self.context.get('user'))


class FeedAddSerializer(Serializer):
    url = URLField(required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def to_representation(self, instance):
        serializer = FeedSerializer(instance)
        return serializer.data
