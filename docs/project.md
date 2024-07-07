# Project API Request Response

A project is the top level container for any tasks that can be associated with the task.
Each project needs a unique code so that the subsequent tasks can be named accordingly.

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
        'email': 'creator@email.com'
    },
    'created_at': <datetime>,
    'modified_at': <datetime>,
    'status': 'DRAFT'
}]
```