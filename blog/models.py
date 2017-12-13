from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Blog(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)
    owner = models.OneToOneField(User, related_name='blog', on_delete=models.CASCADE)
    subscriptions = models.ManyToManyField(User, related_name='subscriptions', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:dashboard', args=[self.owner.username])


class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    blog = models.ForeignKey(Blog, related_name='blog_posts', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='post_owner', on_delete=models.CASCADE)
    body = models.TextField()
    viewed = models.ManyToManyField(User, related_name='viewed', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail', args=[self.owner.username, self.slug])
