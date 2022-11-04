

class FeedFetchFailedException(Exception):
    def __init__(self, msg='Failed to fetch the feed', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
