from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet  # Import your actual viewsets

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'posts', PostViewSet)  # Register PostViewSet
router.register(r'comments', CommentViewSet)  # Register CommentViewSet

urlpatterns = [
    path('api/', include(router.urls)),  # Include the router-generated URLs
]
