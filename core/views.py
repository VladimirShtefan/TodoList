from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.serializers import UserCreateSerializer, UserLoginSerializer, UserProfileSerializer, \
    UserUpdatePasswordSerializer


@method_decorator(csrf_exempt, name="dispatch")
class CreateUserView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)


@method_decorator(csrf_exempt, name="dispatch")
class UserLoginView(CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        login(self.request, user=serializer.save())


class UserProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        logout(self.request)


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdatePasswordView(UpdateAPIView):
    serializer_class = UserUpdatePasswordSerializer

    def get_object(self):
        return self.request.user
