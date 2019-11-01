from django.urls import path
from .views import *

urlpatterns = [

    path('api/v1/fileloads/', FileLoad.as_view()),
    path('profiles', ProfileView.as_view()),
    path('profiles/<int:pk>', ProfileDetailView.as_view()),
    path('profile-post', ProfilePostView.as_view()),
    path('profile-post/<int:pk>', ProfilePostDetailView.as_view()),
    path('posts-comments', PostCommentView.as_view()),
    path('posts-comments/<int:pk>', PostCommentDetailView.as_view()),
    path('servidor/posts/<int:pk>/comments', CommentView.as_view()),
    path('servidor/posts/<int:post_pk>/comments/<int:comment_pk>', CommentDetailView.as_view()),

]
