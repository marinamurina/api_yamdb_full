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
        slug_field='title',
        read_only=True,
    )
    author = SlugRelatedField(
        slug_field='author',
        read_only=True,
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                title=title, author=author
            ).exists:
                raise ValidationError(
                    'Вы можете добавить только один отзыв на произведение.'
                )
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = (
            'name',
            'slug',
        )
        lookup_field = ('slug',)


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = (
            'name',
            'slug',
        )
        lookup_field = ('slug',)


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    
    category = CategoriesSerializer()
    """
    serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all(),
        required=True)"""

    genre = GenresSerializer(many=True, required=False)
    """
    serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
        many=True,
        required=True
    )"""

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
        slug_field='review',
        read_only=True,
    )
    author = SlugRelatedField(
        slug_field='author',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = '__all__'


"""  Вариант Марины
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)
"""

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True,)


    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def validate(self, attrs):
        if attrs['username'] == 'me':
            raise serializers.ValidationError("У пользователя не может быть имени me")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


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

class UserChangeSerializer(serializers.ModelSerializer):
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

class EmailSerializer(serializers.Serializer):
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

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                "У пользователя не может быть имени me"
            )
        return value


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
