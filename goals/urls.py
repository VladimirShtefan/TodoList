from django.urls import path

from goals.views import CreateGoalsCategoryView, GoalCategoryListView, GoalCategoryView

urlpatterns = [
    path('goal_category/create', CreateGoalsCategoryView.as_view(), name='goal_category_create'),
    path("goal_category/list", GoalCategoryListView.as_view(), name='goal_category_list'),
    path("goal_category/<pk>", GoalCategoryView.as_view(), name='goal_category'),
]
