from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializers import PatchVerificationSerializer
from bot.tg.client import TgClient
from todolist.settings import TOKEN_TELEGRAM_BOT


class VerificationCodeView(UpdateAPIView):
    queryset = TgUser.objects.all()
    serializer_class = PatchVerificationSerializer

    def update(self, request, *args, **kwargs) -> Response:
        """
        Исключено получение объекта пользователя, пользователь пробрасывается из сериализатора
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        """
        Изменен для выдачи сообщения пользователю в телеграм бот
        :param serializer:
        :return:
        """
        tg_user: TgUser = serializer.save()
        TgClient(TOKEN_TELEGRAM_BOT).send_message(chat_id=tg_user.tg_id,
                                                  text='Привязка телеграмм аккаунта выполнена успешно'
                                                  )
        return super().perform_update(serializer)

    def put(self, request, *args, **kwargs):
        """
        Запрещенный метод
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        raise MethodNotAllowed(request.method)
