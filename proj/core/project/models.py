# -*- coding: utf-8 -*-

from datetime import datetime
from django.contrib.contenttypes import generic
from taggit.managers import TaggableManager
from proj.core.models import User
from proj.core.comment.models import Comment
from .managers import *

PROJECT_STATUSES = (
    ('open', u'Открыт'),
    ('closed', u'Закрыт'),
)
PUBLIC_STATUSES = (
    ('public', u'Доступен всем'),
    ('friends', u'Доступен только подписчикам'),
    ('community', u'Доступен сообществам'),
    ('private', u'Приватный'),
)


class Project(models.Model):
    reporter = models.ForeignKey(User, related_name='projects', verbose_name=u'Заказчик')

    title = models.CharField(max_length=255, verbose_name=u'Заголовок')
    description = models.TextField(max_length=1000, blank=True, null=True, verbose_name=u'Описание')
    status = models.CharField(max_length=10, choices=PROJECT_STATUSES, default='open', verbose_name=u'Статус')
    visible = models.CharField(max_length=10, choices=PUBLIC_STATUSES, default='public', verbose_name=u'Видимость')

    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    date_due = models.DateTimeField(blank=True, null=True, verbose_name=u'Срок выполнения')
    date_updated = models.DateTimeField(auto_now=True, verbose_name=u'Дата обновления')
    tags = TaggableManager(blank=True)
    comments = generic.GenericRelation(Comment)

    def __unicode__(self):
        return self.title

    @property
    def is_past_due(self):
        if datetime.now() > self.date_due:
            return True
        return False


class Milestone(models.Model):
    project = models.ForeignKey(Project, related_name='milestones', verbose_name=u'Веха')

    title = models.CharField(max_length=255, verbose_name=u'Заголовок')
    description = models.TextField(max_length=1000, blank=True, null=True, verbose_name=u'Описание')

    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    date_due = models.DateTimeField(blank=True, null=True, verbose_name=u'Срок выполнения')
    date_updated = models.DateTimeField(auto_now=True, verbose_name=u'Дата обновления')

    objects = MilestoneManager()

    def __unicode__(self):
        return self.title

    @property
    def is_past_due(self):
        if datetime.now() > self.date_due:
            return True
        return False

