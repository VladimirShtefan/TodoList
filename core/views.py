from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.models import User
from core.serializers import UserCreateSerializer, UserLoginSerializer, UserProfileSerializer, \
    UserUpdatePasswordSerializer


class CreateUserView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)


class UserLoginView(CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs) -> Response:
        """
        Исключил формирование headers
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer) -> None:
        """
        Происходит логин пользователя через cookies
        :param serializer:
        :return:
        """
        login(self.request, user=serializer.save())


class UserProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self) -> User:
        """
        Получение текущего пользователя из request
        :return:
        """
        return self.request.user

    def perform_destroy(self, instance) -> None:
        """
        Удаление из cookies данных о пользователе
        :param instance:
        :return:
        """
        logout(self.request)


class UserUpdatePasswordView(UpdateAPIView):
    serializer_class = UserUpdatePasswordSerializer

    def get_object(self) -> User:
        """
        Получение текущего пользователя из request
        :return:
        """
        return self.request.user
