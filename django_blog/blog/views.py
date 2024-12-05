from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .forms import ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        # Use UserChangeForm to update basic user details (email, username)
        form = UserChangeForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        
        if form.is_valid() and profile_form.is_valid():
            form.save()  # Save user data (email, username)
            profile_form.save()  # Save profile data (bio, profile_picture)
            return redirect('profile')  # Redirect to the same page after saving
    else:
        # Prepopulate the forms with the current user's details
        form = UserChangeForm(instance=user)
        profile_form = ProfileUpdateForm(instance=user.profile)
    
    return render(request, 'registration/profile.html', {'form': form, 'profile_form': profile_form})