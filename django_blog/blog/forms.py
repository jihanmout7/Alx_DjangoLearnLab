from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment
from taggit.forms import TagField  # Import the TagField from django-taggit

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        
class PostForm(forms.ModelForm):
    tags = TagField(required=False)  # Use TagField to handle the tags input
    class Meta:
        model = User
        fields = '__all__'
        
    def validate(self, data):
        if len(data['title']) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return data    
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # Explicitly choose which fields to display in the form
        fields = ['content']  # Only show the content field in the form