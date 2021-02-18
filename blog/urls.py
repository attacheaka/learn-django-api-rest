from rest_framework import routers
from .api import CategoriesViewSet, ArticlesViewSet

router = routers.DefaultRouter()
router.register('api/categories', CategoriesViewSet, 'categories')
router.register('api/articles', ArticlesViewSet, 'articles')

urlpatterns = router.urls