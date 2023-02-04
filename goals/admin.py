from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment, Board


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    search_fields = ('title', 'user__username')
    list_filter = ('created', 'updated')
    readonly_fields = ('created', 'updated')


class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'due_date', 'status', 'priority', 'description')
    search_fields = ('title', 'description', 'category__name')
    list_filter = ('created', 'updated')
    readonly_fields = ('created', 'updated')


class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'goal')
    list_filter = ('created', 'updated')
    readonly_fields = ('created', 'updated')


class BoardAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('created', 'updated')
    readonly_fields = ('created', 'updated')


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
admin.site.register(Board, BoardAdmin)
