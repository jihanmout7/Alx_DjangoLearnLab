from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserLoginSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import UserProfile , CustomUser
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def follow_user(request, user_id):
    """
    Allow authenticated users to follow another user.
    """
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        # Get the target user
        target_user = User.objects.get(id=user_id)
        target_profile = target_user.profile
        
        # Get the current user's profile
        current_profile = request.user.profile
        
        # Prevent the user from following themselves
        if current_profile == target_profile:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Add target user to the following list
        current_profile.following.add(target_profile)
        return Response({"detail": f"Now following {target_user.username}."}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def unfollow_user(request, user_id):
    """
    Allow authenticated users to unfollow another user.
    """
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        # Get the target user
        target_user = User.objects.get(id=user_id)
        target_profile = target_user.profile
        
        # Get the current user's profile
        current_profile = request.user.profile
        
        # Prevent the user from unfollowing themselves
        if current_profile == target_profile:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Remove target user from the following list
        current_profile.following.remove(target_profile)
        return Response({"detail": f"Unfollowed {target_user.username}."}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class Meta :
    model = CustomUser
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]