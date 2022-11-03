from django.db import models
from django.contrib.auth import get_user_model
from activity.models import Read, Like, Bookmark, LikeMixin, ReadMixin, BookmarkMixin
from .managers import FeedManager, ArticleManager

User = get_user_model()


class Feed(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    rss_url = models.URLField(unique=True)
    follows = models.ManyToManyField(User)

    objects = FeedManager()

    def follow(self, user: User):
        self.follows.add(user)

    def set_articles(self, articles):
        for article in articles:
            article.feed = self

    def __str__(self):
        return f'Feed: {self.name} - {self.rss_url}'


class Article(ReadMixin,
              LikeMixin,
              BookmarkMixin,
              models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    author = models.CharField(max_length=100, null=True, blank=True)
    link = models.URLField(unique=True)
    publish_date = models.DateTimeField()
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    objects = ArticleManager()

    def is_read(self, user: User):
        read = Read(user=user)
        self.reads.add(read, bulk=False)

    def is_bookmarked(self, user: User):
        bookmark = Bookmark(user=user)
        self.bookmarks.add(bookmark, bulk=False)

    def __str__(self):
        return f'Article: {self.title} - {self.link}'
