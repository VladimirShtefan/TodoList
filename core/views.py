from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView

from core.models import User
from core.serializers import UserCreateSerializer


@method_decorator(csrf_exempt, name="dispatch")
class CreateUser(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
