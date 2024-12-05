from django.db import models
from django.contrib.auth.models import User  # Import the User model

class Post(models.Model):
    title = models.CharField(max_length=200)  # The title of the post
    content = models.TextField()  # The content of the post
    published_date = models.DateTimeField(auto_now_add=True)  # The publication date, auto set when the post is created
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to the User model (handles one-to-many relationship)

    def __str__(self):
        return self.title  # Return the title when the object is printed
