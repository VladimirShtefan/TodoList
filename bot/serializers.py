from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bot.models import TgUser


class PatchVerificationSerializer(serializers.ModelSerializer):
    def validate_verification_code(self, verification_code: str) -> str | None:
        """
        Валидация проверочного кода введенного пользователем
        :param verification_code:
        :return:
        """
        try:
            self.instance = TgUser.objects.get(verification_code=verification_code)
        except TgUser.DoesNotExist:
            raise ValidationError('Не верный код')
        return verification_code

    def update(self, instance: TgUser, validated_data: dict) -> TgUser:
        """
        Запись пользователя в базу TgUser.user_id
        :param instance:
        :param validated_data:
        :return:
        """
        self.instance.user = self.context['request'].user
        return super().update(instance, validated_data)

    class Meta:
        model = TgUser
        fields = '__all__'
        read_only_fields = ('username', 'tg_id', 'user')
        