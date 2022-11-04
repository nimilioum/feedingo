from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta
from article.models import Feed, Article

User = get_user_model()


class ArticleTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='john')

        self.feed1 = Feed.objects.create(name='mag', description='mag', rss_url='https://mag.com/rss')
        self.feed1.follow(user=self.user)
        self.feed2 = Feed.objects.create(name='mag2', description='mag', rss_url='https://mag.com/rss2')

        self.article1 = Article.objects.create(title='a1', description='a1', link='https://mag.com/a1',
                                               feed=self.feed1, publish_date=now())
        self.article2 = Article.objects.create(title='a2', description='a2', link='https://mag.com/a2',
                                               feed=self.feed1, publish_date=now() - timedelta(100))
        self.article3 = Article.objects.create(title='a3', description='a3', link='https://mag.com/a3',
                                               feed=self.feed2, publish_date=now() - timedelta(200))

    def test_get_user_feeds(self):
        feeds = Feed.objects.get_user_feed_ids(self.user)

        self.assertEqual(len(feeds), 1)
        self.assertEqual(feeds[0], self.feed1.id)

    def test_get_user_feed_items(self):
        feeds = Feed.objects.get_user_feed_ids(self.user)
        items = Article.objects.get_user_feed_items(self.user, feeds)

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].id, self.article1.id)
        self.assertEqual(items[1].id, self.article2.id)

    def test_get_user_feed_items_read(self):
        feeds = Feed.objects.get_user_feed_ids(self.user)
        items = Article.objects.get_user_feed_items(self.user, feeds)

        self.article1.read(self.user)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].id, self.article2.id)

    def test_get_liked_items(self):
        self.article1.like(self.user)
        self.article2.like(self.user)

        articles = Article.objects.get_liked_items(self.user)

        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0].id, self.article1.id)
        self.assertEqual(articles[1].id, self.article2.id)

    def test_get_bookmarked_items(self):
        self.article2.bookmark(self.user)
        self.article3.bookmark(self.user)

        articles = Article.objects.get_bookmarked_items(self.user)

        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0].id, self.article2.id)
        self.assertEqual(articles[1].id, self.article3.id)
