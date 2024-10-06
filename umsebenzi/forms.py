from django import forms
from umsebenzi.models import Task
from umsebenzi.latest import get_task_code


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('code',)

    def save(self, commit=True):
        task = super().save(commit=False)
        if not self.instance.id:
            project = self.cleaned_data['project']
            count = get_task_code(project)
            task.code = f'{project.code}-{count}'
        task.save()
        return task
