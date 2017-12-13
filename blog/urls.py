from django.urls import path

from blog.views import HomeView, PostDetailView, NewPostView, PostUpdate, PostDelete

app_name = 'blog'
urlpatterns = [
    path('<str:user>/', HomeView.as_view(), name='dashboard'),
    path('<str:user>/new-post/', NewPostView.as_view(), name='new-post'),
    path('<str:user>/<slug:slug>/update/', PostUpdate.as_view(), name='update-post'),
    path('<str:user>/<slug:slug>/delete/', PostDelete.as_view(), name='delete-post'),
    path('<str:user>/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
]