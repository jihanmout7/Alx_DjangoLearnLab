from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.views import LoginView, LogoutView
from .models import Profile


# Custom Login Form
class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the form, e.g., changing widget attributes
        self.fields['username'].widget.attrs.update({'placeholder': 'Your username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Your password'})

# Custom Login View
class CustomLoginView(LoginView):
    form_class = CustomLoginForm  # Use your custom login form
    template_name = 'registration/login.html'  # Specify your custom template

# Custom User Registration Form with Email Validation
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already in use.')
        return email

# User Registration View
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Saves the new user to the database
            messages.success(request, 'Account created successfully!')
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

# Custom Logout View
class CustomLogoutView(LogoutView):
    next_page = 'home'  # Redirect to the homepage after logging out

# Define the forms in views.py

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']  # Fields from the Profile model

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']  # Only the email field from the User model

@login_required
def profile_view(request):
    # Get the current user's profile or create one if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Handle form submission (POST request)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user form and profile form
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')  # Redirect to the profile page after success
    else:
        # Pre-fill the forms with the current user's information
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })