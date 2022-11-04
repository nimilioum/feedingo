from django.urls import  path,include
from rest_framework.routers import DefaultRouter
from .views import FeedViewSet, ArticleViewSet

router = DefaultRouter()
router.register('feeds', FeedViewSet, basename='feeds')
router.register('articles', ArticleViewSet, basename='articles')

urlpatterns = [
    path('', include(router.urls)),
]
