from django.urls import path

from goals.views import CreateGoalsCategoryView, GoalCategoryListView, GoalCategoryView, CreateGoalView, GoalsListView, \
    GoalView, CreateCommentView, CommentsListView, CommentView

urlpatterns = [
    path('goal_category/create', CreateGoalsCategoryView.as_view(), name='goal_category_create'),
    path("goal_category/list", GoalCategoryListView.as_view(), name='goal_category_list'),
    path("goal_category/<int:pk>", GoalCategoryView.as_view(), name='goal_category'),
    path('goal/create', CreateGoalView.as_view(), name='goal_create'),
    path("goal/list", GoalsListView.as_view(), name='goals_list'),
    path("goal/<pk>", GoalView.as_view(), name='goal'),
    path('goal_comment/create', CreateCommentView.as_view(), name='goal_comment_create'),
    path("goal_comment/list", CommentsListView.as_view(), name='goal_comment_list'),
    path("goal_comment/<int:pk>", CommentView.as_view(), name='goal_comment'),
]
