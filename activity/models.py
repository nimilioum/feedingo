from django.db import models, IntegrityError
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from utils.exceptions import DomainException, FeedFetchFailedException

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

    def read(self, user: User):
        try:
            read = Read(user=user)
            self.reads.add(read, bulk=False)
        except IntegrityError:
            pass


class Like(Activity):
    pass


class LikeMixin(models.Model):
    class Meta:
        abstract = True

    likes = GenericRelation(Like)

    def like(self, user: User):
        try:
            like = Like(user=user)
            self.likes.add(like, bulk=False)
        except IntegrityError:
            raise DomainException('object is already liked')

    def unlike(self, user: User):
        try:
            content_type = ContentType.objects.get_for_model(self.__class__)
            like = Like.objects.get(content_type__pk=content_type.id, object_id=self.id, user=user)
            self.likes.remove(like)
        except Like.DoesNotExist:
            raise DomainException('object is not liked')


class Bookmark(Activity):
    pass


class BookmarkMixin(models.Model):
    class Meta:
        abstract = True

    bookmarks = GenericRelation(Bookmark)

    def bookmark(self, user: User):
        try:
            bookmark = Bookmark(user=user)
            self.bookmarks.add(bookmark, bulk=False)
        except IntegrityError:
            raise DomainException('object is already bookmarked')

    def unbookmark(self, user: User):
        try:
            content_type = ContentType.objects.get_for_model(self.__class__)
            bookmark = Bookmark.objects.get(content_type__pk=content_type.id, object_id=self.id, user=user)
            self.bookmarks.remove(bookmark)
        except Bookmark.DoesNotExist:
            raise DomainException('object is not bookmarked')


class Comment(Activity):
    message = models.TextField()


class CommentMixin(models.Model):
    class Meta:
        abstract = True

    comments = GenericRelation(Comment)

    def add_comment(self, user: User, message):
        comment = Comment(user=user, message=message)
        self.comments.add(comment, bulk=False)
