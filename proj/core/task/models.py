# -*- coding: utf-8 -*-

from django.db import models
from proj.core.models import User
from proj.core.project.models import Project
from proj.core.community.models import Community

STATUSES_CHOICES = (
    ('new', u'Новая задача'),
    ('open', u'Открыта'),
    ('resolved', u'Выполнена'),
    ('closed', u'Закрыта'),
)
PUBLIC_STATUSES = (
    ('public', u'Доступна всем'),
    ('friends', u'Доступна только подписчикам'),
    ('community', u'Доступна сообществам'),
    ('private', u'Приватная'),
)


class Task(models.Model):
    parent = models.ForeignKey('self', related_name='sub_tasks', verbose_name=u'Родительская задача')
    reporter = models.ForeignKey(User, related_name='reported_tasks', verbose_name=u'Заказчик')
    assignee = models.ForeignKey(User, related_name='assigned_tasks', blank=True, null=True,
                                 verbose_name=u'Исполнитель')
    project = models.ForeignKey(Project, related_name='tasks', blank=True, null=True,
                                verbose_name=u'Проект')
    status = models.CharField(max_length=10, choices=STATUSES_CHOICES, default='new', verbose_name=u'Статус')
    title = models.CharField(max_length=255, verbose_name=u'Название')
    content = models.TextField(max_length=1000, blank=True, null=True, verbose_name=u'Суть задачи')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    date_due = models.DateTimeField(blank=True, null=True, verbose_name=u'Срок выполнения')
    date_updated = models.DateTimeField(auto_now=True, verbose_name=u'Дата обновления')
    visible = models.CharField(max_length=10, choices=PUBLIC_STATUSES, default='public',
                               verbose_name=u'Доступность')
    communities = models.ManyToManyField(Community, related_name='tasks', blank=True, null=True,
                                         verbose_name=u'Опубликовать в сообществах')

    class Meta:
        verbose_name = u'Задача'
        verbose_name_plural = u'Задачи'

