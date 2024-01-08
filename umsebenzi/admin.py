from django.contrib import admin

from umsebenzi.models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'code', 'status', 'created_by', 'created_at')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('project', 'code', 'title', 'description', 'status',
                    'created_by', 'assigned_to', 'created_at'
                    )
