from django.core.validators import RegexValidator
from rest_framework import serializers
from .models import User, Article


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_author', 'is_subscriber']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            RegexValidator(
                regex=r'^[\w\.-]+@[\w\.-]+\.\w+$',
                message='Enter a valid email address.'
            )
        ]
    )
    password = serializers.CharField(
        write_only=True,
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
                message='Password must be at least 8 characters long and contain at least one letter and one number.'
            )
        ]
    )
    is_author = serializers.BooleanField(required=False)
    is_subscriber = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'is_author', 'is_subscriber']

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        is_author = validated_data.get('is_author', False)
        is_subscriber = validated_data.get('is_subscriber', False)
        user = User(
            email=email,
            username=email,
            is_author=is_author,
            is_subscriber=is_subscriber
        )

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists!."})

        user.set_password(password)
        user.save()
        return user


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'is_public']
