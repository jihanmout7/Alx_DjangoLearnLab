from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserLoginSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate

# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer




class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    