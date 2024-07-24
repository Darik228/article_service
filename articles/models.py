from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_author = models.BooleanField(default=False)
    is_subscriber = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.id}. {self.email} Author-{self.is_author} Subscriber-{self.is_subscriber}'


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}. "{self.title}" {self.author.email} {self.is_public}'
