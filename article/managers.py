from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class FeedManager(models.Manager):

    def get_user_feeds(self, user: User):
        return self.filter(follows=user).values_list('id', flat=True)


class ArticleManager(models.Manager):

    def unread(self, user):
        return self.filter(~Q(reads__user=user))

    def get_user_feed_items(self, user: User, feeds):
        return self.unread(user).filter(feed__in=feeds).order_by('-publish_date')

    def get_by_feed(self, feed):
        return self.filter(feeds_in=feed).order_by('-publish_date')

    def get_liked_items(self, user: User):
        return self.filter(likes__user=user)

    def get_bookmarked_items(self, user: User):
        return self.filter(bookmarks__user=user)
