from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment 
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly  # Import the custom permission
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Notification
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions
from django.utils import timezone
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



@login_required
def like(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the user has already liked the post
    if post.likes.filter(id=user.id).exists():
        # If the user has already liked the post, handle this scenario (e.g., return a message)
        return JsonResponse({'error': 'You have already liked this post.'}, status=400)
    
    # Add the user to the likes
    post.likes.add(user)

    # Create a notification for the user
    notification = Notification.objects.create(
        recipient=post.author,  # The post author is the recipient of the like notification
        actor=user,  # The user who liked the post
        verb="liked",  # Action verb
        target_content_type=ContentType.objects.get_for_model(post),  # The model for the target (Post)
        target_object_id=post.id,  # The post's ID
    )

    # Optionally, you can return a success response or a redirect
    return JsonResponse({'success': 'Post liked successfully!'}, status=200)
    
@login_required
def unlike(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)

    # Check if the user has already liked the post
    if not post.likes.filter(id=user.id).exists():
        # If the user has not liked the post, handle this scenario (e.g., return a message)
        return JsonResponse({'error': 'You have not liked this post.'}, status=400)

    # Remove the like from the post
    post.likes.remove(user)

    # Optionally, you can also create a notification for unliking or handle it differently.

    return JsonResponse({'success': 'Post unliked successfully!'}, status=200)
        
    
@login_required
def notification(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)

    # Initialize a response variable to store notification type
    response = {}

    # Check if there is a new follower notification
    if user in post.author.followers.all():  # Assuming you have a 'followers' many-to-many relationship
        response['new_follower'] = f"You have a new follower: {user.username}."

    # Check if the user liked the post
    if post.likes.filter(id=user.id).exists():
        response['post_liked'] = f"{user.username} liked your post."

    # Check if there's a new comment on the post
    new_comments = Comment.objects.filter(post=post)
    if new_comments.exists():
        response['new_comment'] = f"{user.username} commented on your post."

    # Return the response as JSON (or render it in a template)
    if response:
        return JsonResponse(response, status=200)
    else:
        return JsonResponse({'message': 'No new notifications'}, status=404)


@login_required
def fetch_notifications(request):
    user = request.user
    
    # Fetch notifications for the logged-in user
    notifications = Notification.objects.filter(recipient=user).order_by('-timestamp')

    # Prepare the notifications to be sent in the response
    response = []
    
    for notification in notifications:
        notification_data = {
            'id': notification.id,
            'actor': notification.actor.username,
            'verb': notification.verb,
            'target': str(notification.target),  # Convert target to string representation
            'timestamp': notification.timestamp,
            'is_read': notification.is_read
        }
        
        # Add a key to mark the notification as unread if it is not read
        if not notification.is_read:
            notification_data['unread'] = True
        else:
            notification_data['unread'] = False

        response.append(notification_data)
    
    return JsonResponse({'notifications': response}, status=200)