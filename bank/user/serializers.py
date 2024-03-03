from django.contrib.auth import authenticate
from rest_framework import serializers, views, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User
from rest_framework.permissions import AllowAny




class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensure password is write-only

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password', 'is_active', 'is_staff', 'is_staff_activated', 'can_add_percentage']

    def create(self, validated_data):
        # Create a new user and hash their password
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # Update user and hash the password
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class UserLoginAPIView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
