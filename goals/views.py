from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalFilter, CommentGoalFilter
from goals.models import GoalCategory, Goal, GoalComment, Board
from goals.permissions import BoardPermissions, GoalCategoryPermissions, GoalPermissions, GoalCommentPermissions
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, \
    GoalSerializer, GoalCommentCreateSerializer, GoalCommentSerializer, BoardCreateSerializer, BoardSerializer


# GoalCategory
class CreateGoalsCategoryView(CreateAPIView):
    queryset = GoalCategory.objects.all()
    serializer_class = GoalCategoryCreateSerializer
    permission_classes = (GoalCategoryPermissions, IsAuthenticated)


class GoalCategoryListView(ListAPIView):
    queryset = GoalCategory.objects.all()
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ('board',)
    ordering_fields = ('title', 'created')
    search_fields = ('title',)
    ordering = ('title',)

    def get_queryset(self):
        return GoalCategory.objects.prefetch_related('board__participants__user').filter(
            board__participants__user_id=self.request.user.id,
            is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    queryset = GoalCategory.objects.all()
    serializer_class = GoalCategorySerializer
    permission_classes = (GoalCategoryPermissions, IsAuthenticated)

    def get_queryset(self):
        return GoalCategory.objects.prefetch_related('board__participants__user').filter(
            board__participants__user_id=self.request.user.id,
            is_deleted=False
        )

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.goal.update(status=Goal.Status.archived)
        return instance


# Goal
class CreateGoalView(CreateAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalCreateSerializer
    permission_classes = (GoalPermissions, IsAuthenticated)


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
        print(1)
        return Goal.objects.prefetch_related('category').filter(
            Q(category__board__participants__user_id=self.request.user.id) &
            ~Q(status=Goal.Status.archived) &
            Q(category__is_deleted=False)
        )


class GoalView(RetrieveUpdateDestroyAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = (GoalPermissions, IsAuthenticated)

    def get_queryset(self):
        return Goal.objects.prefetch_related('category').filter(
            Q(category__board__participants__user_id=self.request.user.id) &
            ~Q(status=Goal.Status.archived) &
            Q(category__is_deleted=False)
        )


# Comment
class CreateCommentView(CreateAPIView):
    queryset = GoalComment.objects.all()
    serializer_class = GoalCommentCreateSerializer
    permission_classes = (GoalCommentPermissions, IsAuthenticated)


class CommentsListView(ListAPIView):
    queryset = GoalComment.objects.all()
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_class = CommentGoalFilter
    ordering_fields = ('created',)
    ordering = ('-created',)

    def get_queryset(self):
        return GoalComment.objects.prefetch_related('goal').filter(
            Q(goal__category__board__participants__user_id=self.request.user.id)
            & ~Q(goal__status=Goal.Status.archived)
            & Q(goal__category__is_deleted=False)
        )


class CommentView(RetrieveUpdateDestroyAPIView):
    queryset = GoalComment.objects.all()
    serializer_class = GoalCommentSerializer
    permission_classes = (GoalCommentPermissions, IsAuthenticated)

    def get_queryset(self):
        return GoalComment.objects.prefetch_related('goal').filter(
            Q(goal__category__board__participants__user_id=self.request.user.id)
            & ~Q(goal__status=Goal.Status.archived)
            & Q(goal__category__is_deleted=False)
        )


# Board
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
    ordering_fields = ('title',)
    ordering = ('title',)

    def get_queryset(self):
        return Board.objects.prefetch_related('participants').filter(
            Q(is_deleted=False) & Q(participants__user_id=self.request.user.id)
        )


class BoardView(RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (BoardPermissions, IsAuthenticated)

    def get_queryset(self):
        return Board.objects.prefetch_related('participants').filter(
            Q(is_deleted=False) & Q(participants__user_id=self.request.user.id)
        )

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.goal_category.update(is_deleted=True)
            Goal.objects.prefetch_related('category').filter(category__board_id=instance.id).update(
                status=Goal.Status.archived
            )
        return instance
