# blog/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView  # Import the built-in LoginView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # Use Django's LoginView
    path('logout/', views.logout_view, name='logout'),  # Assuming you have a custom logout view
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
