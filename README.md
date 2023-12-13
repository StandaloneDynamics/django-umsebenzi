# Django-Umsebenzi

Umsebenzi, which means work in the Zulu language,  is a set of Django REST apis to manage and keep track of your personal
projects.

It consists of 2 Endpoints:

* Projects - create a new project
* Tasks - create a task under a project

# Installation
```
pip install django-umsebenzi
```

# Setup

* Add the app `umsebenzi` to `INSTALLED_APPS`
* Umsebenzi comes with its own router `DefaultRouter`. To add it to your main router:
```
from umsebenzi.urls import router as umsebenzi_router 

main_router.registry.extend(umsebenzi_router.registry)
```

Once the urls are connected you will be to view docs if you have the swagger tool for api documentation
There are some examples below to see some of the data that can be created



# Example Request/Response

## Project API
### Request

```
data = {
    'title': 'New Project',
    'description': 'Build stuff here',
    'code': 'NP'
}
self.client.post(self.url, data, format='json')
```
### Response
```
[{
    'id': <project.id>,
    'title': 'New Project,
    'description': 'Build stuff here,
    'code': NP,
    'created_by': {
        'username': 'creator',
        'email': ''
    },
    'created_at': <datetime>,
    'modified_at': <datetime>,
    'status': 'DRAFT'
}]
```


## Task API
### Request
```
data = {
    'project_id': <project.id>,
    'title': 'Write Tests',
    'description': 'Write Tests to finish project',
    'assigned_to_id': <user.id>,
}
```

### Response
```
{
    'project': {
        'id': <project.id>,
        'title': 'New Project',
        'description': 'Build Stuff here',
        'code': 'NP',
        'status': 'DRAFT',
        'created_at': <datetime>,
        'modified_at': <datetime>,
        'created_by': {
            'username': 'creator',
            'email': ''
        }
    },
    'title': 'Write Tests',
    'description': 'Write Tests to finish project',
    'status': 'DRAFT',
    'code': 'NP-1',
    'created_at': <datetime>,
    'modified_at': <datetime>,
    'assigned_to': {
        'username': 'assignee',
        'email': ''
    },
    'created_by': {
        'username': 'creator',
        'email': ''
    }
}
```