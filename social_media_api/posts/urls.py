from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet  # Import your actual viewsets

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'posts', PostViewSet)  # Register PostViewSet
router.register(r'comments', CommentViewSet)  # Register CommentViewSet
router.register(r'feed', /feed/)

urlpatterns = [
    path('api/', include(router.urls)),  
    path('posts/<int:pk>/like/', views.post_like, name='post_like'),
    path('posts/<int:pk>/unlike/', views.post_unlike, name='post_unlike')
]
