from django.contrib import admin

from goals.models import GoalCategory


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user")
    search_fields = ("title", "user__username")
    list_filter = ("created", "updated")
    readonly_fields = ('created', 'updated')


admin.site.register(GoalCategory, GoalCategoryAdmin)
