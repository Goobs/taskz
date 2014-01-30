# -*- coding: utf-8 -*-

from django.db import models


class ProjectManager(models.Manager):
    pass


class MilestoneManager(models.Manager):
    def latest_top(self):
        return self.order_by('-date_updated')[:5]
