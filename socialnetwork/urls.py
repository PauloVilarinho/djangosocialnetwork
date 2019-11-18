from django.urls import path
from .views import *

urlpatterns = [

    path('login/', CustomAuthToken.as_view(), name='login'),
    path('api/v1/fileloads/', FileLoad.as_view(),name='load-files'),
    path('profiles', ProfileView.as_view(),name='profile-list'),
    path('profiles/<int:pk>', ProfileDetailView.as_view(),name='profile-details'),
    path('profile-post', ProfilePostView.as_view(),name= 'profile-post'),
    path('profile-post/<int:pk>', ProfilePostDetailView.as_view(),name='profile-post-details'),
    path('posts-comments', PostCommentView.as_view(),name='post-comments'),
    path('posts-comments/<int:pk>', PostCommentDetailView.as_view(),name='post-comments-detail'),
    path('posts/<int:pk>/comments', CommentView.as_view(),name='comments-list'),
    path('posts/comments/<int:pk>', CommentDetailView.as_view(),name='comment-detail'),
    path('profiles-activity', ProfileActivityView.as_view(),name='profiles-activity'),
    path('root', EndpointsView.as_view(),name='root'),

]
