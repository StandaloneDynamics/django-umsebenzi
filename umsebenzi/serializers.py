from rest_framework import serializers
from django.contrib.auth import get_user_model
from django_enumfield.contrib.drf import NamedEnumField

from umsebenzi.models import Project, Task
from umsebenzi.enums import TaskStatus

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class ProjectSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('created_at', 'modified_at', 'created_by')

    def update(self, instance: Project, validated_data):
        """
        update the tasks code if the projects code has been updated
        """
        if instance.code != validated_data['code']:
            tasks = instance.tasks.filter(project=instance)
            for t in tasks:
                t.code = t.code.replace(instance.code, validated_data['code'])
                t.save()
        return super().update(instance, validated_data)


class TaskSerializer(serializers.ModelSerializer):
    project_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Project.objects.all())
    assigned_to_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all())
    project = ProjectSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    status = NamedEnumField(TaskStatus, required=False, default=TaskStatus.DRAFT)

    class Meta:
        model = Task
        fields = (
            'project_id', 'project', 'title', 'description', 'assigned_to',
            'assigned_to_id', 'created_by', 'status', 'code', 'due_date',
            'created_at', 'modified_at'
        )
        read_only_fields = ('code', 'created_at', 'modified_at')

    def create(self, validated_data):
        project = validated_data.pop('project_id')
        assigned_to = validated_data.pop('assigned_to_id')
        count = Task.objects.filter(project=project).count() + 1
        code = f'{project.code}-{count}'
        return Task.objects.create(
            code=code,
            project=project,
            assigned_to=assigned_to,
            **validated_data
        )

    def update(self, instance: Task, validated_data):
        instance.project = validated_data.get('project_id', instance.project)
        instance.assigned_to = validated_data.get('assigned_to_id', instance.assigned_to)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class TaskStatusSerializer(serializers.ModelSerializer):
    status = NamedEnumField(TaskStatus, required=True)

    class Meta:
        model = Task
        fields = ('status',)
