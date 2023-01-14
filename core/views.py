from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from core.serializers import UserCreateSerializer, UserLoginSerializer


@method_decorator(csrf_exempt, name="dispatch")
class CreateUserView(CreateAPIView):
    serializer_class = UserCreateSerializer


@method_decorator(csrf_exempt, name="dispatch")
class UserLoginView(CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        login(self.request, user=serializer.save())
