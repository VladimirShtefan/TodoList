from django.urls import path

from goals.views import CreateGoalsCategoryView, GoalCategoryListView, GoalCategoryView, CreateGoalView, GoalsListView, \
    GoalView

urlpatterns = [
    path('goal_category/create', CreateGoalsCategoryView.as_view(), name='goal_category_create'),
    path("goal_category/list", GoalCategoryListView.as_view(), name='goal_category_list'),
    path("goal_category/<int:pk>", GoalCategoryView.as_view(), name='goal_category'),
    path('goal/create', CreateGoalView.as_view(), name='goal_create'),
    path("goal/list", GoalsListView.as_view(), name='goals_list'),
    path("goal/<pk>", GoalView.as_view(), name='goal'),
]
