from django.utils.translation import gettext_lazy
from django_enumfield import enum


class TaskStatus(enum.Enum):
    DRAFT = 1
    READY = 2
    TO_DO = 3
    IN_PROGRESS = 4
    REVIEW = 5
    COMPLETE = 6

    __labels__ = {
        DRAFT: gettext_lazy('Draft'),
        READY: gettext_lazy('Ready'),
        TO_DO: gettext_lazy('To Do'),
        IN_PROGRESS: gettext_lazy('In Progress'),
        REVIEW: gettext_lazy('Review'),
        COMPLETE: gettext_lazy('Complete')
    }
