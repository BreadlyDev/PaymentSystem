from rest_framework import serializers
from . import models as m


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = m.User
        fields = ['email', 'password']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = m.User
        fields = ['email', 'password', 'username']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.User
        fields = ['email', 'username']
