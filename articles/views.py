from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Article, User
from .serializers import ArticleSerializer, RegisterSerializer


class PublicArticleList(generics.ListAPIView):
    queryset = Article.objects.filter(is_public=True)
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]


class PrivateArticleList(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_subscriber:
            return Article.objects.filter(is_public=False)
        raise PermissionDenied("Only subscribers can view private articles.")


class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class CreateArticle(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_author:
            raise PermissionDenied("Only authors can create articles.")
        serializer.save(author=user)


class ManageArticle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)
