from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from blog.models import Post, Blog


class GreetingView(ListView):
    template_name = 'greetings.html'
    context_object_name = 'posts'
    model = Post

    def get_queryset(self):
        posts = Post.objects.all()
        return posts


class HomeView(ListView):
    template_name = 'dashboard.html'
    context_object_name = 'posts'
    model = Post

    def get_queryset(self):
        blog = Blog.objects.filter(owner=self.request.user)
        posts = Post.objects.filter(blog=blog[0])
        return posts


class PostDetailView(DetailView):
    template_name = 'post_detail.html'
    model = Post
