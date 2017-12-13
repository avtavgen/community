from django import template
from ..models import Post, Blog

register = template.Library()


@register.inclusion_tag('available_blogs.html')
def available_blogs():
    blogs = Blog.objects.all()
    return {'available_blogs': blogs}
