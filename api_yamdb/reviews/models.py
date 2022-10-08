from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, UserManager, PermissionsMixin, AbstractUser
)
from django.utils.translation import gettext_lazy as _
from django.db import models


SCORE_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
)
ROLE_CHOICES = (
    (1, 'user'),
    (2, 'moderator'),
    (3, 'Admin'),
)

class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True)
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    bio = models.TextField('Биография', blank=True,) 
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=False, unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()
    email_verified=models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this users email is verified '
        ),
    )
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    @property
    def token(self):
        return ''


class Categories(models.Model):
    name = models.CharField(
        max_length=256,
    )

    slug = models.SlugField(unique=True)


class Genres(models.Model):
    name = models.CharField(
        max_length=255,
    )

    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    year = models.IntegerField()

    category = models.ForeignKey(
        Categories,
            on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )

    genre = models.ManyToManyField(
        Genres,
        related_name='titles',
        blank=True
    )


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='review'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='review'
    )
    score = models.CharField(
        max_length=2,
        choices=SCORE_CHOICES,
        default='1',
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text[:settings.FIRST_SYMBOLS_NUMBER]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comment'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comment'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text[:settings.FIRST_SYMBOLS_NUMBER]
