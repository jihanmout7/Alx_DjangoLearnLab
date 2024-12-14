from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, verbose_name="Author", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the post is created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated when the post is modified
    
        class Meta:
        ordering = ['-created_at']
        
        def __str__(self):
            return f"Post by {self.user.username} at {self.created_at}"
class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        unique_together = ('user', 'followed_user')

    def __str__(self):
        return f"{self.user.username} follows {self.followed_user.username}"

class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name="Post", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)  # Automatically set when the comment is created
    updated_at = models.DateField(auto_now=True)  # Automatically updated when the comment is modified

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"


