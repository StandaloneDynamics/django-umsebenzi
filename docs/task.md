## Task API Request Response

A task can be created as either an `EPIC` or `SUBTASK`.
An epic can have multiple subtasks

Subtasks can be treated as tasks as they can have their own statuses and assignees.

### Request
```
data = {
    'project_id': <project.id>,
    'title': 'Write Tests',
    'description': 'Write Tests to finish project',
    'assigned_to_id': <user.id>,
    'issue': 'EPIC'
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
            'email': 'creator@email.com'
        }
    },
    'title': 'Write Tests',
    'description': 'Write Tests to finish project',
    'due_date': None
    'status': 'DRAFT',
    'code': 'NP-1',
    'created_at': <datetime>,
    'modified_at': <datetime>,
    'issue': 'EPIC',
    'assigned_to': {
        'username': 'assignee',
        'email': 'assignee@email.com'
    },
    'created_by': {
        'username': 'creator',
        'email': 'creator@email.com'
    }
    substasks: None
}
```

### Filtering Tasks
Tasks can be filtered by using the project code, example url is shown below.
```
eg: http://localhost:8000/v1/api/tasks?project=<code>
```
