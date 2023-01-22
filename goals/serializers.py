from rest_framework import serializers

from goals.models import GoalCategory, Goal, GoalComment
from core.serializers import UserProfileSerializer


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ('is_deleted', 'created', 'updated')


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("created", "updated")


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_category(self, category):
        if category.is_deleted:
            raise ValidationError('Нельзя создать цель для категории в архиве')
        if self.context['request'].user != category.user:
            raise ValidationError('Вы не являетесь владельцем данной категории')
        return category

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('created', 'updated', 'user')


class GoalSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("created", "updated")


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("created", "updated")


class GoalCommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("created", "updated")
