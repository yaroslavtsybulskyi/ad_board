from rest_framework import serializers
from django.contrib.auth.models import User
from typing import Dict, Any

from board.models import UserProfile


class RegisterSerializer(serializers.Serializer):
    """
    Serializer for registering a new user.
    """

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data: Dict[str, Any]) -> User:
        """
        Creates a new User and associated UserProfile based on the validated data.
        :param validated_data: Validated data containing username, email, and password.
        :return: The created Django User instance.
        """
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']

        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user, email=email)

        return user
