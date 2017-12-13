from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

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

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs['user'])
        blog = Blog.objects.filter(owner=user)
        posts = Post.objects.filter(blog=blog[0])
        ctx['posts'] = posts
        ctx['owner'] = user
        return ctx


class NewPostView(CreateView):
    model = Post
    fields = (
        'title', 'body', 'slug'
    )

    template_name = 'new_post.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NewPostView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        new_post = form.save(commit=False)
        user = User.objects.get(username=self.request.user.username)
        blog = Blog.objects.get(owner=self.request.user)
        new_post.blog = blog
        new_post.owner = user
        new_post.save()
        post_url = self.request.build_absolute_uri(new_post.get_absolute_url())
        subject = '{} ({}) recommends you reading "{}"'.format(user.username, user.email, new_post.title)
        message = 'Read "{}" at {}'.format(new_post.title, post_url, user.username)
        for subscription in blog.subscriptions.all():
            send_mail(subject, message, user.email, [subscription.email])
        self.object = new_post

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('blog:post-detail', args=[self.object.owner.username, self.object.slug])


class PostDetailView(DetailView):
    template_name = 'post_detail.html'
    model = Post


class PostUpdate(UpdateView):
    model = Post
    fields = ['body']
    template_name = 'post_update_form.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('greeting')


class BlogSubscriptionView(View):
    def get(self, request, **kwargs):
        blog = Blog.objects.get(slug=kwargs['slug'])
        blog.subscriptions.add(request.user)
        return HttpResponseRedirect(reverse('greeting'))


class RemoveBlogSubscriptionView(View):
    def get(self, request, **kwargs):
        blog = Blog.objects.get(slug=kwargs['slug'])
        blog.subscriptions.remove(request.user)
        return HttpResponseRedirect(reverse('greeting'))


class NewsFeedView(ListView):
    template_name = 'news_feed.html'
    context_object_name = 'posts'
    model = Post

    def get_context_data(self, **kwargs):
        ctx = super(NewsFeedView, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs['user'])
        posts = []
        for subscription in user.subscriptions.all():
            blog = Blog.objects.get(owner=subscription.owner)
            for post in Post.objects.filter(blog=blog):
                posts.append(post)
        ctx['posts'] = posts
        ctx['owner'] = user
        return ctx
