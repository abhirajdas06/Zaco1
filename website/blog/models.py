from pyexpat import model
from tabnanny import verbose
from unicodedata import category, name
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



# Category
class Category(models.Model):
    name =  models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering =('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
     return self.name

            
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)


# post
class Post(models.Model):
    
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=False)
    image = models.ImageField(upload_to = 'blogs', default="")
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


