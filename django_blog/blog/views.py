from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Profile  # Import the Profile model from the current app



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
    try:
        profile = user.profile  # This will access the related profile for the user
    except Profile.DoesNotExist:
        profile = None  # Handle the case where the user doesn't have a profile

    return render(request, 'profile.html', {'profile': profile})