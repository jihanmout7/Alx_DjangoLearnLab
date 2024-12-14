from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment 
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly  # Import the custom permission

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    queryset = Post.objects.filter(author__in=following_users)
    queryset = Post.objects.filter(author__in=following_users).order_by
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]  # Apply the custom permission
    filter_backends = [SearchFilter]  # Specify the filtering backend
    search_fields = ['title', 'content']  # Specify the fields to search
    permission_classes = permissions.IsAuthenticated

    # Optional: If you want to filter based on other parameters like 'username', you can modify get_queryset.
    def get_queryset(self):
        queryset = Post.objects.all()
        username = self.request.query_params.get('username', None)
        
        if username:
            queryset = queryset.filter(purchaser__username=username)
        
        return queryset
    def perform_create(self, serializer):
        # Associate the created post with the current user
        serializer.save(user=self.request.user)
        
@login_required
def feed(request):
    # Get the current user
    user = request.user
    
    # Get the list of users the current user is following
    following_users = user.following.all()  # All users the current user follows
    
    # Get the posts from the followed users, ordered by creation date
    posts = Post.objects.filter(user__in=following_users).order_by('-created_at')
    
    # Render the feed template with the posts
    return render(request, 'posts/feed.html', {'posts': posts})

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]  # Apply the custom permission

    def perform_create(self, serializer):
        # Associate the created comment with the current user
        serializer.save(user=self.request.user)



 
        