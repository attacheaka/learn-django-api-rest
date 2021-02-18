from django.urls import path, include

urlpatterns = [
    path('', include('blog.urls')),
    path('', include('accounts.urls')),
]