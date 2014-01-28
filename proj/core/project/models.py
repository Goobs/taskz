# -*- coding: utf-8 -*-

from django.db import models
from proj.core.models import User


class Project(models.Model):
    reporter = models.ForeignKey(User, related_name='reported_tasks', verbose_name=u'Заказчик')




