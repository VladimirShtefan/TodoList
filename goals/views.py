from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalFilter, CommentGoalFilter
from goals.models import GoalCategory, Goal, GoalComment, Board
from goals.permissions import BoardPermissions
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, \
    GoalSerializer, GoalCommentCreateSerializer, GoalCommentSerializer, BoardCreateSerializer, BoardSerializer


class CreateGoalsCategoryView(CreateAPIView):
    queryset = GoalCategory.objects.all()
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    queryset = GoalCategory.objects.all()
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
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    queryset = GoalCategory.objects.all()
    serializer_class = GoalCategorySerializer

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted', ))
            instance.goals.update(status=Goal.Status.archived)
        return instance


class CreateGoalView(CreateAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalCreateSerializer


class GoalsListView(ListAPIView):
    queryset = Goal.objects.all()
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
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

    def get_queryset(self):
        return Goal.objects.filter(
            Q(user_id=self.request.user.id) & ~Q(status=Goal.Status.archived) & Q(category__is_deleted=False)
        )


class CreateCommentView(CreateAPIView):
    queryset = GoalComment.objects.all()
    serializer_class = GoalCommentCreateSerializer


class CommentsListView(ListAPIView):
    queryset = GoalComment.objects.all()
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_class = CommentGoalFilter
    ordering_fields = ('created', )
    ordering = ('-created', )

    def get_queryset(self):
        return GoalComment.objects.filter(
            Q(user=self.request.user)
            & ~Q(goal__status=Goal.Status.archived)
            & Q(goal__category__is_deleted=False)
        )


class CommentView(RetrieveUpdateDestroyAPIView):
    queryset = GoalComment.objects.all()
    serializer_class = GoalCommentSerializer

    def get_queryset(self):
        return GoalComment.objects.filter(
            Q(user=self.request.user)
            & ~Q(goal__status=Goal.Status.archived)
            & Q(goal__category__is_deleted=False)
        )


class CreateBoardView(CreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardCreateSerializer


class BoardsListView(ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        OrderingFilter,
    ]
    ordering_fields = ('title', )
    ordering = ('title', )

    def get_queryset(self):
        return Board.objects.filter(
            Q(is_deleted=False) & Q(participants__user=self.request.user)
        )


class BoardView(RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (BoardPermissions, IsAuthenticated)

    def get_queryset(self):
        return Board.objects.filter(
            Q(is_deleted=False) & Q(participants__user=self.request.user)
        )

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.goal_category.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance
