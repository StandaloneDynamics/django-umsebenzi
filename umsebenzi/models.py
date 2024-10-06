from django.db import models
from django.conf import settings

from django_enumfield import enum
from umsebenzi.enums import TaskStatus, Issue


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    code = models.CharField(max_length=10, unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.code} - {self.title}'

    class Meta:
        indexes = [
            models.Index(fields=['title', 'code'])
        ]


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    code = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = enum.EnumField(TaskStatus, default=TaskStatus.DRAFT)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_tasks')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='assigned_tasks')
    issue = enum.EnumField(Issue, default=Issue.EPIC)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.code} - {self.title}'

    class Meta:
        indexes = [
            models.Index(fields=['code'])
        ]
