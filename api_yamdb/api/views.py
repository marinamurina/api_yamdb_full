from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.mixins import UpdateModelMixin
# Свой клас для разделения доступа по ролям
from .permissions import AdminOrReadOnly

from reviews.models import (
    Categories,
    Genres,
    Title,
    Review,
    Comment,
    User,
)

from .serializers import (
    CategoriesSerializer,
    GenresSerializer,
    ReviewSerializer,
    TitleSerializer,
    RegisterSerializer,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    UserChangeSerializer,
)


class GetRetrieveViewSet(
    RetrieveAPIView,
    UpdateModelMixin,
):
    pass


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes =

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=title_id)
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes =

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        new_queryset = Comment.objects.filter(review=review_id)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(
            author=self.request.user,
            review=review
        )


class RegisterAPIView(GenericAPIView):

    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    # permission_classes = (IsAdminUser, )
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'


class UserChangeAPIView(GetRetrieveViewSet):
    serializer_class = UserChangeSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        return User.objects.filter(
            user=get_object_or_404(
                User, id=self.request.user
            )
        )
