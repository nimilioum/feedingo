from rest_framework.exceptions import APIException


class FeedFetchFailedException(APIException):
    status_code = 500
    default_detail = 'Failed to fetch the feed'
    default_code = 'internal service error'


class DomainException(APIException):
    status_code = 400
    default_detail = 'bad request'
    default_code = 'bad request'
