from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from core.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(write_only=True)

    def validate_password(self, password: str) -> str:
        """
        Валидация переданного пароля
        :param password:
        :return:
        """
        validate_password(password)
        return password

    def validate(self, attrs: dict) -> dict:
        """
        Проверка совпадения пароля и его повтора
        :param attrs:
        :return:
        """
        if attrs['password'] != attrs['password_repeat']:
            raise serializers.ValidationError({'password_repeat': 'Пароли должны совпадать'})
        return super().validate(attrs)

    def create(self, validated_data: dict) -> User:
        """
        Установка пароля в базу в шифрованном виде
        :param validated_data:
        :return:
        """
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

    def create(self, validated_data: dict) -> User:
        """
        Проверка логина и пароля на корректность
        :param validated_data:
        :return:
        """
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


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UserUpdatePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, old_password: str) -> str:
        """
        Проверка старого пароля при смене на новый
        :param old_password:
        :return:
        """
        if not self.instance.check_password(old_password):
            raise ValidationError('Пароль не верный')
        return old_password

    def validate_new_password(self, new_password: str) -> str:
        """
        Валидация переданного пароля
        :param new_password:
        :return:
        """
        validate_password(new_password)
        return new_password

    def update(self, instance: User, validated_data: dict) -> User:
        """
        Обновление пароля модели User в базе данных
        :param instance:
        :param validated_data:
        :return:
        """
        instance.set_password(validated_data['new_password'])
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = ('old_password', 'new_password')
