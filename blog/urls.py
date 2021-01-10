
from django.urls import path
from . import views
from blog.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'), #Change here to redirect to Profile, also user_posts.html  bhi kuch change hoga
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'), 
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/' ,  PostCreateView.as_view(), name='post-create'),
    path('feed/', views.feed, name='blog-feed'),
    
]


#     path('followers/<str:username>', 'friend_list', {'list_type': 'followers'}, name='followers_followers'),
#     path('following/<str:username>', 'friend_list', { 'list_type': 'following'}, name='followers_following'),
#     path('mutual/<str:username>', 'friend_list', {'list_type': 'mutual'}, name='followers_mutual'),
#     path('follow/<str:username>', 'follow', name='followers_follow'),
#     path('unfollow/<str:username>', 'unfollow', name='followers_unfollow'),
# ]