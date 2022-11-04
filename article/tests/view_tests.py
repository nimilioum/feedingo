from unittest.mock import patch
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from article.models import Feed, Article

User = get_user_model()


class FeedViewTestCase(APITestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create_user(username='user1', password='randompassword')
        self.user2 = User.objects.create_user(username='user2', password='randompassword', is_superuser=True)

        self.feeds = []
        for i in range(5):
            feed = Feed.objects.create(name=f'feed-{i}', description='feed', rss_url=f'https://feed-{i}.com/rss')
            self.feeds.append(feed)

    def test_access_view_unauthenticated(self):
        response = self.client.get(reverse('feeds-list'))

        self.assertEqual(response.status_code, 401)

    def test_get_all_feeds(self):
        self.client.login(username=self.user1.username, password='randompassword')
        response = self.client.get(reverse('feeds-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(self.feeds))
        for i in range(len(response.data)):
            self.assertEqual(response.data[i]['id'], self.feeds[i].id)

    def test_get_field_by_id(self):
        self.client.login(username=self.user1.username, password='randompassword')
        response = self.client.get(reverse('feeds-detail', kwargs={'pk': self.feeds[2].id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['rss_url'], self.feeds[2].rss_url)

    @patch('article.views.RSSParser')
    def test_add_field_by_rss_url(self, mock_rss):
        data = {'url': 'https://fake-rss.com/rss'}
        feed = Feed(name='fake', description='fake', rss_url=data['url'])
        instance = mock_rss.return_value
        instance.get_feed.return_value = feed
        instance.get_articles.return_value = []

        self.client.login(username=self.user1.username, password='randompassword')
        response = self.client.post(reverse('feeds-add'), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], feed.name)
        self.assertEqual(len(response.data['articles']), 0)

    def test_follow_feed(self):
        self.client.login(username=self.user1.username, password='randompassword')
        response = self.client.post(reverse('feeds-follow', kwargs={'pk': self.feeds[2].id}))

        self.assertEqual(response.status_code, 204)

    def test_followed_feeds(self):
        self.feeds[0].follow(self.user1)
        self.feeds[1].follow(self.user1)

        self.client.login(username=self.user1.username, password='randompassword')
        response = self.client.get(reverse('feeds-followed'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(list(map(lambda x: x['id'], response.data)), [self.feeds[0].id, self.feeds[1].id])

    def test_create_feed_admin(self):
        self.client.login(username=self.user2.username, password='randompassword')
        data = {
            'name': 'feed-6',
            'description': 'feed',
            'rss_url': 'https://feed-6.com/rss'
        }
        response = self.client.post(reverse('feeds-list'), data=data)
        feed = Feed.objects.get(pk=response.data['id'])

        self.assertEqual(response.status_code, 201)
        self.assertEqual(feed.rss_url, data.get('rss_url'))

    def test_create_feed_not_admin(self):
        self.client.login(username=self.user1.username, password='randompassword')
        data = {
            'name': 'feed-6',
            'description': 'feed',
            'rss_url': 'https://feed-6.com/rss'
        }
        response = self.client.post(reverse('feeds-list'), data=data)

        self.assertEqual(response.status_code, 403)


class ArticleViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='user1', password='randompassword')

        self.feeds = []
        self.articles = []

        for i in range(2):
            feed = Feed.objects.create(name=f'feed-{i}', description='feed', rss_url=f'https://feed-{i}.com/rss')
            self.feeds.append(feed)

        for feed in self.feeds:
            for i in range(5):
                article = Article.objects.create(title=f'article-{i}', description='article',
                                                 link=f'{feed.rss_url}/{i}', publish_date=timezone.now(),
                                                 feed=feed)
                self.articles.append(article)

    def test_get_all_articles(self):
        self.client.login(username=self.user.username, password='randompassword')
        response = self.client.get(reverse('articles-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 10)

    def test_get_feed_articles(self):
        self.feeds[0].follow(self.user)
        self.client.login(username=self.user.username, password='randompassword')
        response = self.client.get(reverse('articles-feed'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)
        for article in response.data:
            self.assertEqual(article['feed'], self.feeds[0].id)

    def test_get_article_by_id(self):
        self.client.login(username=self.user.username, password='randompassword')
        response = self.client.get(reverse('articles-detail', kwargs={'pk': self.articles[0].pk}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['link'], self.articles[0].link)

    def test_like_article(self):
        pass

    def test_unlike_article(self):
        pass

    def test_bookmark_article(self):
        pass

    def test_unbookmark_article(self):
        pass

    def test_is_read(self):
        pass
