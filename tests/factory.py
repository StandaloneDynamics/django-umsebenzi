from factory.django import DjangoModelFactory
from factory import SubFactory

from django.contrib.auth.models import User
from umsebenzi.models import Project, Task
from umsebenzi.enums import Issue, TaskStatus


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User


class ProjectFactory(DjangoModelFactory):
    title = 'New Project'
    description = 'A new description'
    code = 'NP'
    created_by = SubFactory(UserFactory)

    class Meta:
        model = Project


class TaskFactory(DjangoModelFactory):
    project = SubFactory(ProjectFactory)
    created_by = SubFactory(UserFactory)
    assigned_to = SubFactory(UserFactory)
    title = 'First Task'
    description = 'Complete task'
    issue = Issue.EPIC
    status = TaskStatus.DRAFT
    code = 'NP-1'

    class Meta:
        model = Task
