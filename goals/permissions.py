from rest_framework import permissions

from goals.models import BoardParticipant, Board, GoalCategory, Goal, GoalComment


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Board) -> bool:
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user_id=request.user.id, board_id=obj.id).exists()
        return BoardParticipant.objects.filter(user_id=request.user.id, board_id=obj.id,
                                               role=BoardParticipant.Role.owner
                                               ).exists()


class GoalCategoryPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: GoalCategory) -> bool:
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user_id=request.user.id, board_id=obj.board.id).exists()
        return BoardParticipant.objects.filter(
            user_id=request.user.id, board_id=obj.board.id,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()


class GoalPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Goal) -> bool:
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user_id=request.user.id, board_id=obj.category.board.id).exists()
        return BoardParticipant.objects.filter(
            user_id=request.user.id, board_id=obj.category.board.id,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()


class GoalCommentPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: GoalComment) -> bool:
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user_id=request.user.id,
                                                   board_id=obj.goal.category.board.id
                                                   ).exists()
        return BoardParticipant.objects.filter(
            user_id=request.user.id, board_id=obj.goal.category.board.id,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()
