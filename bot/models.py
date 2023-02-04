from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import User


class TgUser(models.Model):
    tg_id = models.IntegerField(verbose_name=_('Tg id'))
    username = models.CharField(verbose_name=_('Tg username'), max_length=150, null=True, blank=True)
    verification_code = models.CharField(verbose_name=_('Verification code'), max_length=255, null=True, blank=True)
    user = models.ForeignKey(
        User,
        verbose_name=_('Автор'),
        on_delete=models.CASCADE,
        related_name='tg_user',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Телеграм пользователь')
        verbose_name_plural = _('Телеграм пользователи')

    def __str__(self):
        return self.username
