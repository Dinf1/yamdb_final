from django.db.models import Avg
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Category
        lookup_field = 'slug'

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    text = serializers.CharField(required=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Genre
        lookup_field = 'slug'

    def create(self, validated_data):
        genre = Genre.objects.create(**validated_data)
        return genre


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        is_exist = Review.objects.filter(
            author=self.context['request'].user,
            title=self.context['view'].kwargs.get('title_id')).exists()
        if is_exist and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Пользователь уже оставлял отзыв на это произведение')
        return data


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = [
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        ]
        model = Title

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))['score__avg']


class TitlesPostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=True,
        write_only=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        many=False,
        required=False,
        write_only=True
    )

    year = serializers.DecimalField(
        required=True,
        max_digits=5,
        decimal_places=0
    )

    class Meta:
        model = Title
        fields = '__all__'


class GettingTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class RegistrationSerializer(serializers.ModelSerializer):

    validators = [
        UniqueTogetherValidator(
            queryset=User.objects.all(), fields=["username", "email"]
        )
    ]

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError("Username 'me' is not valid")
        return value

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        confirmation_code = default_token_generator.make_token(self.instance)
        send_mail(
            'Register code',
            f'{confirmation_code}',
            settings.EMAIL,
            [self.instance.email],
        )
        return self.instance

    class Meta:
        fields = ('username', 'email')
        model = User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'bio', 'role')


class TokenSerializer(serializers.ModelSerializer):

    confirmation_code = serializers.CharField(allow_blank=False)
    username = serializers.CharField(max_length=150, allow_blank=False)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
