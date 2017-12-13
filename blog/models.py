from django.contrib.auth.models import User
from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20)
    owner = models.OneToOneField(User, related_name='blog', on_delete=models.CASCADE)
    subscriptions = models.ManyToManyField(User, related_name='subscriptions', blank=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    blog = models.ForeignKey(Blog, related_name='blog_posts', on_delete=models.CASCADE)
    body = models.TextField()
    viewed = models.ManyToManyField(User, related_name='viewed', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
