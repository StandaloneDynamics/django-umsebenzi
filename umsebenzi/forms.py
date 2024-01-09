from django import forms
from umsebenzi.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('code',)

    def save(self, commit=True):
        task = super().save(commit=False)
        if not self.instance.id:
            project = self.cleaned_data['project']
            count = Task.objects.filter(project=project).count() + 1
            task.code = f'{project.code}-{count}'
        task.save()
        return task
