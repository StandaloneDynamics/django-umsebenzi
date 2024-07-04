from rest_framework.test import APITestCase
from django.urls import reverse
from .factory import TaskFactory, ProjectFactory

from django.contrib.auth.models import User

from umsebenzi.models import Project, Task
from umsebenzi.enums import TaskStatus, Issue


class ProjectTestCase(APITestCase):
    url = reverse('project-list')

    def setUp(self) -> None:
        self.creator = User.objects.create(username='creator', password='password')
        self.assignee = User.objects.create(username='assignee', password='password')

        self.project = Project.objects.create(
            title='New Project',
            description='A new description',
            code='NP',
            created_by=self.creator
        )

    def test_required_fields(self):
        data = {}
        self.client.force_login(self.creator)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'code': ['This field is required.'],
            'description': ['This field is required.'],
            'title': ['This field is required.']
        })

    def test_create(self):
        data = {
            'title': 'Example',
            'description': 'Build stuff here',
            'code': 'EX'
        }
        self.client.force_login(self.creator)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Project.objects.count(), 2)

    def test_update(self):
        url = reverse('project-detail', kwargs={'pk': self.project.id})

        data = {
            'title': self.project.title,
            'description': 'New description',
            'code': 'EX'
        }
        self.client.force_login(self.creator)
        resp = self.client.put(url, data, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 'EX')
        self.assertEqual(resp.json()['description'], 'New description')

    def test_delete_created_by(self):
        self.assertEqual(Project.objects.count(), 1)

        url = reverse('project-detail', kwargs={'pk': self.project.id})
        self.client.force_login(self.creator)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Project.objects.count(), 0)

    def test_delete_other_user(self):
        self.assertEqual(Project.objects.count(), 1)

        url = reverse('project-detail', kwargs={'pk': self.project.id})

        self.client.force_login(self.assignee)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Project.objects.count(), 1)

    def test_list(self):
        self.client.force_login(self.creator)
        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{
            'id': self.project.id,
            'title': self.project.title,
            'description': self.project.description,
            'code': self.project.code,
            'created_by': {
                'id': self.project.created_by.id,
                'username': 'creator',
                'email': ''
            },
            'created_at': self.project.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'modified_at': self.project.modified_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }])

    def test_project_code_update(self):
        task = Task.objects.create(
            project=self.project,
            created_by=self.creator,
            assigned_to=self.assignee,
            title='Hello World',
            description='Complete task',
            status=TaskStatus.DRAFT,
            code='NP-1'
        )
        self.assertEqual(task.code, 'NP-1')

        url = reverse('project-detail', kwargs={'pk': self.project.id})

        data = {
            'title': 'New Title',
            'description': self.project.description,
            'code': 'EX'
        }
        self.client.force_login(self.creator)
        resp = self.client.put(url, data, format='json')
        self.assertEqual(resp.status_code, 200)

        task.refresh_from_db()
        self.project.refresh_from_db()

        self.assertEqual(self.project.title, 'New Title')
        self.assertEqual(task.code, 'EX-1')


class TaskTestCase(APITestCase):
    url = reverse('task-list')

    def setUp(self) -> None:
        self.maxDiff = None
        self.creator = User.objects.create(username='creator', password='password')
        self.assignee = User.objects.create(username='assignee', password='password')
        self.client.force_login(self.creator)
        self.project = Project.objects.create(
            title='New Project',
            description='A new description',
            code='NP',
            created_by=self.creator
        )

    def test_required_fields(self):
        data = {}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'assigned_to_id': ['This field is required.'],
            'description': ['This field is required.'],
            'project_id': ['This field is required.'],
            'title': ['This field is required.']
        })

    def test_update(self):
        task = Task.objects.create(
            project=self.project,
            created_by=self.creator,
            assigned_to=self.assignee,
            title='Hello World',
            description='Complete task',
            status=TaskStatus.DRAFT,
            code='PR-1'
        )

        url = reverse('task-detail', kwargs={'code': task.code})
        data = {
            'title': task.title,
            'status': TaskStatus.IN_PROGRESS.name,
            'description': task.description,
            'assigned_to_id': task.assigned_to.id,
            'project_id': task.project.id
        }
        resp = self.client.put(url, data, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['status'], TaskStatus.IN_PROGRESS.name)

    def test_create(self):
        data = {
            'assigned_to_id': self.assignee.id,
            'description': 'Write Tests to finish project',
            'project_id': self.project.id,
            'title': 'Write Tests'
        }
        resp = self.client.post(self.url, data, format='json')
        self.assertEqual(resp.status_code, 201)

        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.latest('id')
        self.assertEqual(resp.json(), {
            'project': {
                'id': 1,
                'title': 'New Project',
                'description': 'A new description',
                'code': 'NP',
                'created_at': self.project.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                'modified_at': self.project.modified_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                'created_by': {
                    'id': self.project.created_by.id,
                    'username': 'creator',
                    'email': ''
                }
            },
            'title': 'Write Tests',
            'description': 'Write Tests to finish project',
            'due_date': None,
            'status': 'DRAFT',
            'code': 'NP-1',
            'issue': 'EPIC',
            'created_at': task.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'modified_at': task.modified_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'assigned_to': {
                'id': task.assigned_to.id,
                'username': 'assignee',
                'email': ''
            },
            'created_by': {
                'id': task.created_by.id,
                'username': 'creator',
                'email': ''
            },
            'subtasks': []
        })

    def test_update_status(self):
        task = Task.objects.create(
            project=self.project,
            created_by=self.creator,
            assigned_to=self.assignee,
            title='Hello World',
            description='Complete task',
            status=TaskStatus.DRAFT,
            code="PR-1"
        )

        url = reverse('task-status', kwargs={'code': task.code})
        data = {'status': 'IN_PROGRESS'}

        self.client.force_login(self.creator)
        resp = self.client.patch(url, data, format='json')
        self.assertEqual(resp.status_code, 200)

        task.refresh_from_db()
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS.value)

    def test_filter(self):
        Project.objects.create(
            title='Example Project',
            description='A new description',
            code='EP',
            created_by=self.creator
        )
        Task.objects.create(
            project=self.project,
            created_by=self.creator,
            assigned_to=self.assignee,
            title='Hello World',
            description='Complete task',
            status=TaskStatus.DRAFT,
            code="NP-1"
        )

        self.assertEqual(Project.objects.count(), 2)
        self.assertEqual(Task.objects.count(), 1)

        url = f'{self.url}?project=EP'
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 0)

        url = f'{self.url}?project=NP'
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)

    def test_exclude_archive(self):
        Task.objects.create(
            project=self.project,
            created_by=self.creator,
            assigned_to=self.assignee,
            title='Hello World',
            description='Complete task',
            status=TaskStatus.DRAFT,
            code="NP-1"
        )
        Task.objects.create(
            project=self.project,
            created_by=self.creator,
            assigned_to=self.assignee,
            title='Hello World',
            description='Complete task',
            status=TaskStatus.ARCHIVE,
            code="NP-2"
        )
        resp = self.client.get(self.url, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)


class SubTasksTestCase(APITestCase):
    url = reverse('task-list')

    def setUp(self) -> None:
        self.maxDiff = None
        self.creator = User.objects.create(username='creator', password='password')
        self.assignee = User.objects.create(username='assignee', password='password')
        self.client.force_login(self.creator)
        self.project = ProjectFactory(created_by=self.creator)
        self.task = TaskFactory(project=self.project, created_by=self.creator, assigned_to=self.assignee)

    def test_epic_parent(self):
        data = {
            'project_id': self.project.id,
            'assigned_to_id': self.assignee.id,
            'parent_id': self.task.id,
            'title': 'First Subtask',
            'description': 'Do stuff here',
        }
        resp = self.client.post(self.url, data, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {'non_field_errors': ['Epic task cannot have parent']})

    def test_subtask_subtask(self):
        subtask = TaskFactory(
            project=self.project, issue=Issue.SUBTASK,
            created_by=self.creator, assigned_to=self.assignee,
            code='NP-100'
        )
        data = {
            'project_id': self.project.id,
            'assigned_to_id': self.assignee.id,
            'parent_id': subtask.id,
            'title': 'First Subtask',
            'description': 'Do stuff here',
            'issue': 'SUBTASK',
        }
        resp = self.client.post(self.url, data, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {'non_field_errors': ['Subtask cannot have subtask parent']})

    def test_subtask(self):
        data = {
            'project_id': self.project.id,
            'assigned_to_id': self.assignee.id,
            'parent_id': self.task.id,
            'title': 'First Subtask',
            'description': 'Do stuff here',
            'issue': 'SUBTASK',
            'parent': self.task.id
        }
        resp = self.client.post(self.url, data, format='json')
        self.assertEqual(resp.status_code, 201)
        task = Task.objects.latest('id')
        self.assertEqual(resp.json(), {
            'title': 'First Subtask',
            'description': 'Do stuff here',
            'due_date': None,
            'status': 'DRAFT',
            'issue': 'SUBTASK',
            'code': 'NP-2',
            'created_at': task.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'modified_at': task.modified_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'assigned_to': {
                'id': task.assigned_to.id,
                'username': 'assignee',
                'email': ''
            },
            'created_by': {
                'id': task.created_by.id,
                'username': 'creator',
                'email': ''
            },
            'project': {
                'code': 'NP',
                'created_at': self.project.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                'modified_at': self.project.modified_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                'created_by': {'email': '', 'id': 1, 'username': 'creator'},
                'description': 'A new description',
                'id': 1,
                'title': 'New Project'
            },
            'subtasks': None
        })

    def test_subtask_list(self):
        subtask = TaskFactory(
            project=self.project, issue=Issue.SUBTASK,
            created_by=self.creator, assigned_to=self.assignee,
            parent=self.task, code='NP-100'
        )
        resp = self.client.get(self.url, format='json')
        self.assertEqual(resp.json(), [
            {
                'assigned_to': {'email': '', 'id': 2, 'username': 'assignee'},
                'code': 'NP-1',
                'created_at': self.task.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                'created_by': {'email': '', 'id': 1, 'username': 'creator'},
                'description': 'Complete task',
                'due_date': None,
                'issue': 'EPIC',
                'modified_at': self.task.modified_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                'project': {'code': 'NP',
                            'created_at': self.project.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                            'created_by': {'email': '', 'id': 1, 'username': 'creator'},
                            'description': 'A new description',
                            'id': 1,
                            'modified_at': self.project.modified_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                            'title': 'New Project'},
                'status': 'DRAFT',
                'subtasks': [{'assigned_to': {'email': '', 'id': 2, 'username': 'assignee'},
                              'code': 'NP-100',
                              'created_at': subtask.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                              'created_by': {'email': '', 'id': 1, 'username': 'creator'},
                              'description': 'Complete task',
                              'due_date': None,
                              'issue': 'SUBTASK',
                              'modified_at': subtask.modified_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                              'parent': 1,
                              'status': 'DRAFT',
                              'title': 'First Task'}],
                'title': 'First Task'}
        ])
