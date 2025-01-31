from django import forms
from umsebenzi.models import Task, Project
from umsebenzi.latest import get_task_code
from umsebenzi.enums import Issue


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('code',)

    def clean(self):
        """
        Rules
        1) If Epic cannot have parent
        2) Parent task must belong to same project
        3) If task is subtask parent cannot be subtask
        """
        data = super().clean()
        issue = data['issue']
        epic: Task = data['parent']

        if issue is Issue.EPIC and epic:
            raise forms.ValidationError("Epic task cannot have parent")

        if issue is Issue.SUBTASK and epic and epic.issue is Issue.SUBTASK:
            raise forms.ValidationError("Subtask parent cannot be subtask")

        project: Project = data['project']
        if epic and project:
            if epic.project != project:
                raise forms.ValidationError("Subtask parent(epic) must belong to same project")

        return data

    def save(self, commit=True):
        task = super().save(commit=False)
        if not self.instance.id:
            project = self.cleaned_data['project']
            count = get_task_code(project)
            task.code = f'{project.code}-{count}'
        task.save()
        return task
