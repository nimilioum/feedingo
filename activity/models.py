from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()


class Activity(models.Model):
    class Meta:
        abstract = True
        unique_together = (('user', 'content_type', 'object_id',),)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class ActivityMixin(models.Model):
    class Meta:
        abstract = True


class Read(Activity):
    pass


class ReadMixin(models.Model):
    class Meta:
        abstract = True

    reads = GenericRelation(Read)

    def is_read(self, user: User):
        read = Read(user=user)
        self.reads.add(read, bulk=False)


class Like(Activity):
    pass


class LikeMixin(models.Model):
    class Meta:
        abstract = True

    likes = GenericRelation(Like)

    def is_liked(self, user: User):
        like = Like(user=user)
        self.likes.add(like, bulk=False)

    def is_unliked(self, user: User):
        content_type = ContentType.objects.get_for_model(self.__class__)
        like = Like.objects.get(content_type__pk=content_type.id, object_id=self.id, user=user)
        self.likes.remove(like)


class Bookmark(Activity):
    pass


class BookmarkMixin(models.Model):
    class Meta:
        abstract = True

    bookmarks = GenericRelation(Bookmark)

    def is_bookmarked(self, user: User):
        bookmark = Bookmark(user=user)
        self.bookmarks.add(bookmark, bulk=False)

    def is_unbookmarked(self, user: User):
        content_type = ContentType.objects.get_for_model(self.__class__)
        bookmark = Bookmark.objects.get(content_type__pk=content_type.id, object_id=self.id, user=user)
        self.bookmarks.remove(bookmark)
