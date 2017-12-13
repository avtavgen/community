"""community URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import login, logout, logout_then_login
from django.urls import path, include

from blog.views import GreetingView, BlogSubscriptionView, RemoveBlogSubscriptionView, NewsFeedView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('logout-then-login/', logout_then_login, name='logout_then_login'),
    path('blog/', include('blog.urls', namespace='blog')),
    path('', GreetingView.as_view(), name='greeting'),
    path('subscribe/<slug:slug>/', BlogSubscriptionView.as_view(), name='add-subscription'),
    path('subscribe/<slug:slug>/remove/', RemoveBlogSubscriptionView.as_view(), name='remove-subscription'),
    path('<str:user>/feed/', NewsFeedView.as_view(), name='news-feed'),
]
