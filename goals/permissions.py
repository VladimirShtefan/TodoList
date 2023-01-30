from rest_framework import permissions

from goals.models import BoardParticipant, Board


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Board):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user_id=request.user.id, board_id=obj.id).exists()
        return BoardParticipant.objects.filter(user_id=request.user.id, board_id=obj.id,
                                               role=BoardParticipant.Role.owner
                                               ).exists()


class GoalPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user_id=request.user.id, board_id=obj.board.id).exists()
        return BoardParticipant.objects.filter(
            user_id=request.user.id, board_id=obj.board.id,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()
