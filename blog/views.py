from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from blog.models import Post, Blog


class GreetingView(View):
    message = "Good Day"
    template_name = 'greetings.html'

    def get(self, request):
        return render(request, self.template_name, {'message': self.message})


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
