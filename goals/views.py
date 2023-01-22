from django.db import transaction
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalFilter
from goals.models import GoalCategory, Goal
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, GoalSerializer


@method_decorator(csrf_exempt, name="dispatch")
class CreateGoalsCategoryView(CreateAPIView):
    queryset = GoalCategory.objects.all()
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        OrderingFilter,
        SearchFilter,
    ]
    ordering_fields = ('title', 'created')
    search_fields = ('title',)
    ordering = ('title',)

    def get_queryset(self):
        return GoalCategory.objects.filter(is_deleted=False)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCategorySerializer

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted', ))
            instance.goals.update(status=Goal.Status.archived)
        return instance


@method_decorator(csrf_exempt, name="dispatch")
class CreateGoalView(CreateAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalCreateSerializer


class GoalsListView(ListAPIView):
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_class = GoalFilter
    search_fields = ('title', 'description')

    def get_queryset(self):
        return Goal.objects.filter(
            Q(user_id=self.request.user.id) & ~Q(status=Goal.Status.archived) & Q(category__is_deleted=False)
        )


class GoalView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer

    def get_queryset(self):
        return Goal.objects.filter(
            Q(user_id=self.request.user.id) & ~Q(status=Goal.Status.archived) & Q(category__is_deleted=False)
        )
