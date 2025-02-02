from django.contrib import admin

from umsebenzi.models import Project, Task
from umsebenzi.forms import TaskForm


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'code', 'created_by', 'created_at')


class SubTaskInline(admin.TabularInline):
    model = Task
    fields = ('code', 'title', 'description', 'status')

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'project', 'code', 'title', 'description', 'status', 'issue',
        'created_by', 'assigned_to', 'created_at'
    )
    list_filter = ['project']
    form = TaskForm
    inlines = [SubTaskInline]
