from celery import shared_task
from article.models import Feed, Article
from utils.exceptions import FeedFetchFailedException
from .services import RSSParser


@shared_task()
def get_feed_entries():
    feeds = Feed.objects.all()

    for feed in feeds:
        try:
            parser = RSSParser(feed.rss_url)
            articles = parser.get_articles()

            feed.add_articles(articles)
            Article.objects.bulk_create(articles, ignore_conflicts=True)

        except FeedFetchFailedException:
            continue
