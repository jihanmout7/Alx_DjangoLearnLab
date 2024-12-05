from django.db import models
from django.contrib.auth.models import User  # Import the User model

class Post(models.Model):
    title = models.CharField(max_length=200)  # The title of the post
    content = models.TextField()  # The content of the post
    published_date = models.DateTimeField(auto_now_add=True)  # The publication date, auto set when the post is created
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to the User model (handles one-to-many relationship)

    def __str__(self):
        return self.title  # Return the title when the object is printed
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return self.user.username
    
    
class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")  # Add related_name to easily access comments from the Post model
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model
    content = models.TextField()  # Comment content
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the comment is created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically update when the comment is modified

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"