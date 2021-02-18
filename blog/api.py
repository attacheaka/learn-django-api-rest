from .models import Article, Category
from rest_framework import viewsets, generics, permissions
from .serializers import CategorySerializer, ArticleSerializer, GetArticleSerializer
from .permissions import IsOwner

# Category Viewset
# Category list ( Admin , User , Anonymous )
# Category Post , Update , Delete ( Admin )
class CategoriesViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    def get_permissions(self):
        permission_classes = []

        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create' or self.action == 'update' \
             or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Category.objects.all()
        slug = self.request.query_params.get('slug')
        if slug is not None:
            queryset = queryset.filter(slug=slug)
        return queryset


# Article Viewset
class ArticlesViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return GetArticleSerializer
        return ArticleSerializer

    def get_permissions(self):
        permission_classes = []

        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create' or self.action == 'update' \
             or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Article.objects.all()
        status = self.request.query_params.get('status')
        category = self.request.query_params.get('category')
        author = self.request.query_params.get('author')
        slug = self.request.query_params.get('slug')
        if slug is not None:
            queryset = queryset.filter(slug=slug)
        if status is not None:
            queryset = queryset.filter(status=status)
        if category is not None:
            queryset = queryset.filter(category=category)
        if author == 'owner':
            queryset = queryset.filter(owner=self.request.user)
        return queryset