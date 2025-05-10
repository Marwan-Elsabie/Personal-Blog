from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView,
    PostUpdateView, PostDeleteView, add_comment,
    delete_comment, logged_in_user_profile, profile, profile_update, toggle_like, toggle_follow , toggle_bookmark , notifications, saved_posts
)

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<uuid:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<uuid:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<uuid:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<uuid:pk>/comment/', add_comment, name='add-comment'),
    path('comment/<uuid:pk>/delete/', delete_comment, name='delete-comment'),
    path('profile/', logged_in_user_profile, name='my-profile'),  # For the logged-in user's profile
    path('profile/update/', profile_update, name='profile-update'),
    path('post/<uuid:pk>/like/', toggle_like, name='toggle-like'),
    path('post/<uuid:pk>/bookmark/', toggle_bookmark, name='toggle-bookmark'),
    path('user/<str:username>/', profile, name='profile'),  # For other users' profiles
    path('user/<str:username>/follow/', toggle_follow, name='toggle-follow'),
    path('notifications/', notifications, name='notifications'),
    path('profile/saved-posts/', saved_posts, name='saved-posts'),
]