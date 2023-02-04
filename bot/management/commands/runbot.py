import os

from django.core.management.base import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from todolist.settings import TOKEN_TELEGRAM_BOT


class Command(BaseCommand):
    help = "Run telegram-bot"

    def __init__(self):
        super().__init__()
        self.tg_client = TgClient(TOKEN_TELEGRAM_BOT)
        self.tg_user = TgUser

    @staticmethod
    def _get_verification_code() -> hex:
        return os.urandom(16).hex()

    def _add_verification_code(self, chat_id, username, verification_code: hex) -> None:
        self.tg_user.objects.filter(tg_id=chat_id, username=username).update(verification_code=verification_code)

    def _check_user(self, username: str, chat_id: int) -> int | None:
        tg_user, _ = self.tg_user.objects.get_or_create(tg_id=chat_id, username=username)
        return tg_user.user_id

    def handle(self, *args, **options):
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                chat_id = item.message.chat.id
                username = item.message.from_.username
                if self._check_user(username, chat_id):
                    self.tg_client.send_message(chat_id=chat_id, text=f'Привет {username}')
                else:
                    verification_code = self._get_verification_code()
                    self.tg_client.send_message(chat_id=chat_id, text=f'Подтвердите, пожалуйста, свой аккаунт. '
                                                                      f'Для подтверждения необходимо ввести код: '
                                                                      f'{verification_code} '
                                                                      f'на сайте vshtefan.ga')
                    self._add_verification_code(chat_id, username, verification_code)

