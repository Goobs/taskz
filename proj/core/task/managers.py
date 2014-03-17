# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q


class TaskManager(models.Manager):

    def latest_top(self):
        return self.order_by('-date_updated')[:5]

    def search(self, **kwargs):
        qs = self.all()
        if kwargs.get('project'):
            qs = qs.filter(project_id=kwargs.get('project'))
        if kwargs.get('milestone'):
            qs = qs.filter(milestone_id=kwargs.get('milestone'))
        if kwargs.get('status'):
            qs = qs.filter(status=kwargs.get('status'))
        query = kwargs.get('query')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(tags__name__icontains=query)
            )
        return qs
