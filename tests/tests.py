from rest_framework.test import APITestCase
from django.urls import reverse

from django.contrib.auth.models import User

from umsebenzi.models import Project, Task
from umsebenzi.enums import TaskStatus, ProjectStatus


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
            'description': self.project.description,
            'status': ProjectStatus.IN_PROGRESS.name,
            'code': 'EX'
        }
        self.client.force_login(self.creator)
        resp = self.client.put(url, data, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 'EX')
        self.assertEqual(resp.json()['status'], ProjectStatus.IN_PROGRESS.name)

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
                'username': 'creator',
                'email': ''
            },
            'created_at': self.project.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'modified_at': self.project.modified_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'status': 'DRAFT'
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
            'status': ProjectStatus.IN_PROGRESS.name,
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
            status=TaskStatus.DRAFT
        )

        url = reverse('task-detail', kwargs={'pk': task.id})
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
                'status': 'DRAFT',
                'created_at': self.project.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                'modified_at': self.project.modified_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                'created_by': {
                    'username': 'creator',
                    'email': ''
                }
            },
            'title': 'Write Tests',
            'description': 'Write Tests to finish project',
            'status': 'DRAFT',
            'code': 'NP-1',
            'created_at': task.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'modified_at': task.modified_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'assigned_to': {
                'username': 'assignee',
                'email': ''
            },
            'created_by': {
                'username': 'creator',
                'email': ''
            },
        })
