# Django-Umsebenzi

Umsebenzi, which means work in the Zulu language, is a set of simple Django REST apis to manage and keep track of your personal
projects and tasks.

It consists of 2 Endpoints:

* Projects
* Tasks

# Installation
```
pip install django-umsebenzi
```

# Setup

* Add the app `umsebenzi` to `INSTALLED_APPS`
* Umsebenzi uses `DefaultRouter` for its urls. To add it to your main router in your project:
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
    'due_date': None
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

### Filtering Tasks
Tasks can be filtered by using the project code, example url is shown below.
```
eg: http://localhost:8000/v1/api/tasks?project=<code>
```

# OpenAPI Endpoints

![screenshot of endpoints](api_endpoints.png)