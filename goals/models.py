from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import User


class GoalCategory(models.Model):
    title = models.CharField(verbose_name=_('Название'), max_length=255)
    user = models.ForeignKey(User, verbose_name=_('Автор'), on_delete=models.PROTECT, related_name='goal_category')
    is_deleted = models.BooleanField(verbose_name=_('Удалена'), default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.title
