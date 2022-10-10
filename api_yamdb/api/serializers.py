from rest_framework import serializers

from django.db.models import Avg
from rest_framework.validators import UniqueValidator

from rest_framework.relations import SlugRelatedField
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from reviews.models import (
    Categories,
    Genres,
    Title,
    User,
    Review,
    Comment,
)


class ReviewSerializer(serializers.ModelSerializer):
    title = SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                title=title, author=author
            ).exists():
                raise ValidationError(
                    'Вы можете добавить только один отзыв на произведение.'
                )
        return data

    class Meta:
        model = Review
        fields = (
            'id',
            'author',
            'title',
            'score',
            'text',
            'pub_date'
        )


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = (
            'name',
            'slug',
        )


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = (
            'name',
            'slug',
        )


class ShowTitlesSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(many=True, required=False)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def get_rating(self, obj):
        """Подсчитываем средний рейтинг произведения из отзывов."""
        print(obj.category)
        rating = obj.review.aggregate(Avg('score'))['score__avg']

        if rating is not None:
            rating = int(rating)

        return rating


class CreateUpdateTitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all(),
        required=True,
    )

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def get_rating(self, obj):
        """Подсчитываем средний рейтинг произведения из отзывов."""

        rating = obj.review.aggregate(Avg('score'))['score__avg']

        if rating is not None:
            rating = int(rating)

        return rating


class CommentSerializer(serializers.ModelSerializer):
    review = SlugRelatedField(
        slug_field='text',
        read_only=True,
    )
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = '__all__'


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='Такой имеил уже есть в базе')
        ]
    )
    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='Такое имя уже есть в базе')
        ]
    )

    def validate(self, attrs):
        if attrs['username'] == 'me':
            raise serializers.ValidationError("Uncorrect username")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_field = ('role')
