from django.db import models
from django.utils.text import slugify
from django.conf import settings
# STATUS
STATUS = (
    (0,"Bouillon"),
    (1,"Enligne")
)

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        return super(Category,self).save(*args,**kwargs)

    class Meta:
        ordering = ['created_at']


class Article(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100,blank=True)
    content = models.TextField()
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True)
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING, blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Article, self).save(*args, **kwargs)

    class Meta:
        ordering = ['created_at']
