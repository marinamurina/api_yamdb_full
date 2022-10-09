from rest_framework import routers
from django.urls import path, include

from .views import (
    CategoriesViewSet,
    GenresViewSet,
    ReviewViewSet,
    TitleViewSet,
    RegisterAPIView,
    ReviewViewSet,
    CommentViewSet,
    UserViewSet,
    get_jwt_token,
)


router = routers.DefaultRouter()
router.register(r'v1/categories', CategoriesViewSet)
router.register(r'v1/genres', GenresViewSet)

router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')
router.register(r'v1/titles', TitleViewSet)
router.register(r'v1/users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', RegisterAPIView.as_view()),
    path('v1/auth/token/', get_jwt_token),
    path('', include(router.urls)),
]
