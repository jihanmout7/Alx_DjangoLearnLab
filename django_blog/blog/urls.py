from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView  # Use built-in LoginView and LogoutView
from . import views  
from .views import PostListView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView
from .views import CommentCreateView , CommentDeleteView , CommentDetailView , CommentListView ,CommentUpdateView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # Use Django's built-in LoginView
    path('logout/', LogoutView.as_view(), name='logout'),  # Use Django's built-in LogoutView
    path('register/', views.register, name='register'),  # Your custom register view
    path('profile/', views.profile, name='profile'),  # Your custom profile view
]


urlpatterns = [
    path('', PostListView.as_view(), name='blog_post_list'),
    path("post/new/", PostCreateView.as_view(), name='blog_post_create'),
    path('<int:pk>/', PostDetailView.as_view(), name='blog_post_detail'),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name='blog_post_edit'),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name='blog_post_delete'),
]


urlpatterns = [
    path('', CommentListView.as_view(), name='blog_comment_list'),
    path("post/<int:pk>/comments/new/", CommentCreateView.as_view(), name='blog_commet_create'),
    path('<int:pk>/',CommentDetailView.as_view(), name='blog_comment_detail'),
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name='blog_comment_edit'),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name='blog_comment_delete'),
]