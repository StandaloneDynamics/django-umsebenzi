from umsebenzi.models import Task, Project
from umsebenzi.exceptions import TaskCodeException


def get_task_code(project : Project) -> int:
    """Get latest projects task code and increment by 1"""
    try:
        task = Task.objects.filter(project=project).latest('id')
        code = int(task.code.split('-')[-1])
        return code + 1
    except (IndexError, ValueError):
        raise TaskCodeException
    except Task.DoesNotExist:
        return 1
