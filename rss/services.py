import feedparser
from django.utils.timezone import datetime
from time import mktime
from article.models import Feed, Article
from utils.exceptions import FeedFetchFailedException


class RSSParser:
    def __init__(self, link):
        self.link = link

        self.feed = None
        self.articles = []

        self.parse()

    def parse(self):
        for i in range(3):
            if self.feed is None or not self.feed:
                parser = feedparser.parse(self.link)
                self.feed = parser.feed
                self.articles = parser.entries

    def get_feed(self):
        if not self.feed:
            raise FeedFetchFailedException()

        return Feed(name=self.feed.title,
                    description=self.feed.description,
                    link=self.feed.link,
                    rss_url=self.link)

    def get_articles(self):
        if not self.feed:
            raise FeedFetchFailedException()

        articles = []

        for i in self.articles:
            date = datetime.fromtimestamp(mktime(i.published_parsed))
            articles.append(Article(title=i.title,
                                    description=i.description,
                                    author=i.get('author'),
                                    link=i.link,
                                    publish_date=date))

        return articles
