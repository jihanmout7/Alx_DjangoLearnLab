from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        
    # Example of custom validation method for the whole serializer
    def validate(self, data):
        # Add any custom validation logic for the Post model here
        # Example: ensure the title is not empty or other validation logic
        if 'title' in data and not data['title']:
            raise serializers.ValidationError("Title cannot be empty.")
        return data

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        
    # Example of custom validation method for the whole serializer
    def validate(self, data):
        # Add any custom validation logic for the Comment model here
        # Example: check if the comment text is not empty
        if 'text' in data and not data['text']:
            raise serializers.ValidationError("Comment text cannot be empty.")
        return data
