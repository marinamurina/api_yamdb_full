from rest_framework import routers
from django.urls import path, include

from .views import (
    CategoriesViewSet,
    GenresViewSet,
    ReviewViewSet,
    TitleViewSet,
    RegistrationAPIView,
)


router = routers.DefaultRouter()
router.register(r'v1/categories', CategoriesViewSet)
router.register(r'v1/genres', GenresViewSet)
router.register(r'v1/titles', TitleViewSet)
router.register(r'v1/reviews', ReviewViewSet)

urlpatterns = [
    path('v1/users/', RegistrationAPIView.as_view()),
    path('', include(router.urls)),
]
