from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from core.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(write_only=True)

    def validate_password(self, password):
        validate_password(password)
        return password

    def validate(self, attrs):
        if attrs['password'] != attrs['password_repeat']:
            raise serializers.ValidationError({'password_repeat': 'Пароли должны совпадать'})
        return super().validate(attrs)

    def create(self, validated_data):
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')
        extra_kwargs = {
            'password': {'write_only': True},
        }


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)

    def create(self, validated_data):
        if user := authenticate(
                username=validated_data['username'],
                password=validated_data['password']
        ):
            return user
        raise AuthenticationFailed('Не верный логин или пароль')

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        read_only_fields = ('id', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'password': {'write_only': True},
        }
