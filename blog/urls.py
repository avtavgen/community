from django.urls import path

from blog.views import HomeView, PostDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='dashboard'),
    # path('new-post/', NewPostView.as_view(), name='new-post'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    # path('subscribe/slug:slug/', UpvotePostView.as_view(), name='add-subscription'),
    # path('subscribe/slug:slug/remove/', RemoveUpvoteFromPostView.as_view(), name='remove-subscription'),
]