from rest_framework import routers
from django.urls import path, include

from .views import (
    CategoriesViewSet,
    GenresViewSet,
    TitleViewSet,
    RegistrationAPIView,
    ReviewViewSet,
    CommentViewSet
)


router = routers.DefaultRouter()
router.register(r'v1/categories', CategoriesViewSet)
router.register(r'v1/genres', GenresViewSet)
router.register(r'v1/titles', TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/users/', RegistrationAPIView.as_view()),
    path('', include(router.urls)),
]
