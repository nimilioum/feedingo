from django.test import TestCase
from unittest.mock import patch
from utils.exceptions import FeedFetchFailedException
from .services import RSSParser


class RSSTestCase(TestCase):

    @patch('rss.services.feedparser')
    def test_calling_feed_parser(self, mocked_class):
        mocked_class.parse.return_value.feed = 'something'
        RSSParser('fake_link')
        mocked_class.parse.assert_called_once()
        mocked_class.parse.assert_called_with('fake_link')

    @patch('rss.services.feedparser')
    def test_calling_feedparser_wrong_url(self, mocked_class):
        mocked_class.parse.return_value.feed = {}
        RSSParser('fake_link')
        self.assertEqual(mocked_class.parse.call_count, 3)
        mocked_class.parse.assert_called_with('fake_link')

    @patch('rss.services.feedparser')
    def test_get_feed_handle_wrong_url(self, mocked_class):
        mocked_class.parse.return_value.feed = {}
        parser = RSSParser('fake_link')
        with self.assertRaises(FeedFetchFailedException):
            parser.get_feed()

    @patch('rss.services.feedparser')
    def test_get_articles_handle_wrong_url(self, mocked_class):
        mocked_class.parse.return_value.feed = {}
        parser = RSSParser('fake_link')
        with self.assertRaises(FeedFetchFailedException):
            parser.get_articles()
