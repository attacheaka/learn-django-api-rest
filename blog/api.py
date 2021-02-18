from .models import Category, Article
from rest_framework import viewsets
from .serializers import CategorySerializer, ArticleSerializer

# Category Viewset
class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Article Viewset
class ArticlesViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer