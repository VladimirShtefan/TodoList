from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from goals.models import GoalCategory
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer


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
    ordering_fields = ("title", "created")
    search_fields = ("title",)
    ordering = ("title",)

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCategorySerializer

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
