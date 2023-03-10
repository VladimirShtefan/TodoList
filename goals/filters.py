import django_filters
from django.db.models import DateField
from django_filters.rest_framework import FilterSet

from goals.models import Goal, GoalComment, GoalCategory


class GoalFilter(FilterSet):
    class Meta:
        model = Goal
        fields = {
            'category': ('exact', 'in'),
            'priority': ('exact', 'in'),
            'due_date': ('lte', 'gte'),
        }

        filter_overrides = {
            DateField: {'filter_class': django_filters.IsoDateTimeFilter},
        }


class CommentGoalFilter(FilterSet):
    class Meta:
        model = GoalComment
        fields = {
            "goal": ('exact',)
        }


class GoalCategoryFilter(FilterSet):
    class Meta:
        model = GoalCategory
        fields = {
            "board": ('exact',)
        }
