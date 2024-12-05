# urls.py
from django.urls import path
from .views import register, CustomLoginView, CustomLogoutView, profile_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
]
