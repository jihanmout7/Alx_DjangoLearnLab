from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(max_length=100)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'phone_number', 'bio', 'password', 'password2']
        extra_kwargs = {
            'email': {'required': True, 'validators': [UniqueValidator(queryset=get_user_model().objects.all())]},
        }

    def validate(self, data):
        # Ensure that password2 matches password
        if data['password'] != data['password2']:
            raise ValidationError({"password2": "The two password fields didn't match."})
        return data

    def create(self, validated_data):
        # Remove password2 since it's only for confirmation
        validated_data.pop('password2')

        # Create the user
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number'],
            bio=validated_data.get('bio', '')
        )

        # Create a token for the user after they are successfully created
        token = Token.objects.create(user=user)

        return {
            'user': user,
            'token': token.key  # Return the token key (JWT or Auth token)
        }
