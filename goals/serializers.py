from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import ValidationError

from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant
from core.serializers import UserProfileSerializer
from core.models import User


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_board(self, board: Board):
        if board.is_deleted:
            raise ValidationError('Нельзя создать категорию для доски в архиве')
        if not BoardParticipant.objects.filter(
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer),
            board_id=board.id,
            user_id=self.context['request'].user.id
        ):
            raise ValidationError('У вас нет доступа для создания категорий в данной доске')
        return board

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ('is_deleted', 'created', 'updated')


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    board = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ('created', 'updated')


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_category(self, category: GoalCategory):
        if category.is_deleted:
            raise ValidationError('Нельзя создать цель для категории в архиве')
        if not BoardParticipant.objects.filter(
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer),
            board_id=category.board_id,
            user_id=self.context['request'].user.id
        ):
            raise ValidationError('У вас нет доступа для создания целей в данной категории')
        return category

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('created', 'updated', 'user')


class GoalSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('created', 'updated')


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_goal(self, goal: Goal):
        if goal.category.is_deleted:
            raise ValidationError('Нельзя создать комментарий для категории в архиве')
        if not BoardParticipant.objects.filter(
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer),
            board_id=goal.category.board_id,
            user_id=self.context['request'].user.id
        ):
            raise ValidationError('У вас нет доступа для создания комментариев для данной цели')
        return goal

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('created', 'updated')


class GoalCommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('created', 'updated')


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        with transaction.atomic():
            user = validated_data.pop('user')
            board = Board.objects.create(**validated_data)
            BoardParticipant.objects.create(user_id=user.id, role=BoardParticipant.Role.owner, board_id=board.id)
        return board

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('is_deleted', 'created', 'updated')


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.Role.choices[1:]
    )
    user = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = '__all__'
        read_only_fields = ('created', 'updated', 'board')


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_participants(self, participants):
        for participant in participants:
            if participant['role'] == BoardParticipant.Role.owner:
                raise ValidationError('Нельзя изменить владельца доски')
        return participants

    def update(self, instance: Board, validated_data):
        owner: User = validated_data.pop('user')
        participants = validated_data.pop('participants')
        actual_participants: QuerySet[BoardParticipant] = instance.participants.exclude(user=owner)
        new_participants_data: dict = {participant['user'].id: participant for participant in participants}
        with transaction.atomic():
            for participant in actual_participants:
                participant_id = participant.user.id
                participant_role = participant.role

                if participant_id not in new_participants_data:
                    participant.delete()
                elif participant_role != new_participants_data[participant_id]['role']:
                    participant.role = new_participants_data[participant_id]['role']
                    participant.save()
                del new_participants_data[participant_id]

            for participant_object in new_participants_data.values():
                BoardParticipant.objects.create(
                    board=instance,
                    user=participant_object['user'],
                    role=participant_object['role']
                )

            if title := validated_data.get('title'):
                instance.title = title
                instance.save()
        return instance

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('is_deleted', 'created', 'updated')
