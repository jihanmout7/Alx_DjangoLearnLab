from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView  # Use built-in LoginView and LogoutView
from . import views  # Your custom views (for register, profile, etc.)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # Use Django's built-in LoginView
    path('logout/', LogoutView.as_view(), name='logout'),  # Use Django's built-in LogoutView
    path('register/', views.register, name='register'),  # Your custom register view
    path('profile/', views.profile, name='profile'),  # Your custom profile view
]
