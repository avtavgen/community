from django import template
from ..models import Post, Blog

register = template.Library()


@register.inclusion_tag('available_blogs.html')
def available_blogs(*args, **kwargs):
    current_user = kwargs['current_user']
    if current_user.username:
        blogs = Blog.objects.all().exclude(owner=current_user)
    else:
        blogs = Blog.objects.all()
    return {'available_blogs': blogs}
