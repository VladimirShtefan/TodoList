from django.contrib.auth.hashers import make_password
from factory import Faker, fuzzy, SubFactory, post_generation
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from goals.models import BoardParticipant


@register
class UserFactory(DjangoModelFactory):
    username = Faker('user_name')
    password = Faker('password')

    class Meta:
        model = 'core.User'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        kwargs['password'] = make_password(kwargs['password'])
        return super(UserFactory, cls)._create(model_class, *args, **kwargs)


@register
class BoardFactory(DjangoModelFactory):
    title = Faker('text')

    class Meta:
        model = 'goals.Board'

    @post_generation
    def owner(self, create, owner, **kwargs):
        if not create:
            return
        if owner:
            BoardParticipant.objects.create(board=self, user=owner, role=BoardParticipant.Role.owner)


@register
class BoardParticipantFactory(DjangoModelFactory):
    role = fuzzy.FuzzyChoice(BoardParticipant.Role.choices[1:], getter=lambda role: role[0])
    user = SubFactory(UserFactory)
    board = SubFactory(BoardFactory)

    class Meta:
        model = 'goals.BoardParticipant'
