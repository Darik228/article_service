from django.urls import path
from .views import PublicArticleList, PrivateArticleList, RegisterUser, CreateArticle, ManageArticle

urlpatterns = [
    path('articles/public/', PublicArticleList.as_view(), name='public-article-list'),
    path('articles/private/', PrivateArticleList.as_view(), name='private-article-list'),
    path('register/', RegisterUser.as_view(), name='register-user'),
    path('articles/create/', CreateArticle.as_view(), name='create-article'),
    path('articles/manage/<int:pk>/', ManageArticle.as_view(), name='manage-article'),
]

