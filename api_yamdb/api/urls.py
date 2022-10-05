from rest_framework import routers
from django.urls import path, include

from .views import (
    CategoriesViewSet,
    GenresViewSet,
    TitleViewSet,
    RegistrationAPIView,
)


router = routers.DefaultRouter()
router.register(r'v1/categories', CategoriesViewSet)
router.register(r'v1/genres', GenresViewSet)
router.register(r'v1/titles', TitleViewSet)

urlpatterns = [
    path('v1/users/', RegistrationAPIView.as_view()),
    path('', include(router.urls)),
]
