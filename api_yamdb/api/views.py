from rest_framework import viewsets

from reviews.models import (
    Categories,
    Genres,
    Title,
)

from .serializers import (
    CaregoriesSerializer,
    GenresSerializer,
    TitleSerializer,
)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CaregoriesSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
