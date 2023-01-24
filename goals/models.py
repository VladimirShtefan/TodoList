from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import User


class CreateUpdateDateModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Board(CreateUpdateDateModel):
    is_deleted = models.BooleanField(verbose_name=_('Удалена'), default=False)
    title = models.CharField(verbose_name=_('Название'), max_length=255)

    class Meta:
        verbose_name = _('Доска')
        verbose_name_plural = _('Доски')

    def __str__(self):
        return self.title


class BoardParticipant(CreateUpdateDateModel):
    class Role(models.IntegerChoices):
        owner = 1, 'Владелец'
        writer = 2, 'Редактор'
        reader = 3, 'Читатель'

    role = models.SmallIntegerField(choices=Role.choices, default=Role.owner, verbose_name=_('Роль'))
    user = models.ForeignKey(
        User, verbose_name=_('Участник'),
        on_delete=models.PROTECT, related_name='participants'
    )
    board = models.ForeignKey(
        Board, verbose_name=_('Доска'),
        on_delete=models.PROTECT, related_name='participants'
    )

    class Meta:
        unique_together = ('board', 'user')
        verbose_name = _('Участник')
        verbose_name_plural = _('Участники')

    def __str__(self):
        return self.user.username


class GoalCategory(CreateUpdateDateModel):
    title = models.CharField(verbose_name=_('Название'), max_length=255)
    user = models.ForeignKey(User, verbose_name=_('Автор'), on_delete=models.PROTECT, related_name='goal_category')
    is_deleted = models.BooleanField(verbose_name=_('Удалена'), default=False)
    board = models.ForeignKey(Board, verbose_name=_('Доска'), on_delete=models.PROTECT, related_name="goal_category")

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.title


class Goal(CreateUpdateDateModel):
    class Status(models.IntegerChoices):
        to_do = 1, 'К выполнению'
        in_progress = 2, 'В процессе'
        done = 3, 'Выполнено'
        archived = 4, 'Архив'

    class Priority(models.IntegerChoices):
        low = 1, 'Низкий'
        medium = 2, 'Средний'
        high = 3, 'Высокий'
        critical = 4, 'Критический'

    user = models.ForeignKey(User, verbose_name=_('Автор'), on_delete=models.PROTECT, related_name='goal')
    title = models.CharField(verbose_name=_('Название'), max_length=255)
    description = models.TextField(verbose_name=_('Описание'), null=True, blank=True)
    due_date = models.DateField(verbose_name=_('Дата выполнения'), null=True, blank=True)
    status = models.SmallIntegerField(choices=Status.choices, default=Status.to_do, verbose_name=_('Статус'))
    priority = models.SmallIntegerField(choices=Priority.choices, default=Priority.low, verbose_name=_('Приоритет'))
    category = models.ForeignKey(GoalCategory, verbose_name=_('Категория'), on_delete=models.CASCADE,
                                 related_name='goal')

    class Meta:
        verbose_name = _('Цель')
        verbose_name_plural = _('Цели')

    def __str__(self):
        return self.title


class GoalComment(CreateUpdateDateModel):
    user = models.ForeignKey(User, verbose_name=_('Автор'), on_delete=models.PROTECT, related_name='goal_comment')
    text = models.TextField(verbose_name=_('Текст'))
    goal = models.ForeignKey(Goal, verbose_name=_('Цель'), on_delete=models.CASCADE, related_name='goal_comment')

    class Meta:
        verbose_name = _('Комментарий')
        verbose_name_plural = _('Комментарии')

    def __str__(self):
        return self.text
