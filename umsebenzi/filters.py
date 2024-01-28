from django_filters import rest_framework as filters

from umsebenzi.models import Task


class TaskFilter(filters.FilterSet):
    project = filters.CharFilter(field_name='project__code', lookup_expr='exact')

    class Meta:
        model = Task
        fields = ['project']
