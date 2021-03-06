# -*- coding: utf-8 -*-

from datetime import datetime
from taggit.managers import TaggableManager
from proj.core.models import User, Currency
from proj.core.project.models import Project, Milestone
from proj.core.community.models import Community
from proj.core.comment.models import *
from .managers import *


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
TASK_PRIORITIES = (
    ('blocker', u'Блокирующий'),
    ('critical', u'Критичный'),
    ('major', u'Повышенный'),
    ('minor', u'Пониженный'),
    ('trivial', u'Обычный'),
)


class Task(models.Model):
    parent = models.ForeignKey('self', related_name='sub_tasks', blank=True, null=True,
                               verbose_name=u'Родительская задача')
    reporter = models.ForeignKey(User, related_name='reported_tasks', verbose_name=u'Заказчик')
    repliers = models.ManyToManyField(User, related_name='replied_tasks', blank=True, null=True,
                                      verbose_name=u'Отклики')
    assignee = models.ForeignKey(User, related_name='assigned_tasks', blank=True, null=True,
                                 verbose_name=u'Исполнитель')
    project = models.ForeignKey(Project, related_name='tasks', blank=True, null=True,
                                verbose_name=u'Проект')
    milestone = models.ForeignKey(Milestone, related_name='tasks', blank=True, null=True,
                                  verbose_name=u'Веха')
    status = models.CharField(max_length=10, choices=STATUSES_CHOICES, default='new', verbose_name=u'Статус')
    priority = models.CharField(max_length=10, choices=TASK_PRIORITIES, default='major', verbose_name=u'Приоритет')
    title = models.CharField(max_length=255, verbose_name=u'Название')
    description = models.TextField(max_length=1000, blank=True, null=True, verbose_name=u'Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Стоимость')
    currency = models.ForeignKey(Currency, default='RUB', verbose_name=u'Валюта')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    date_due = models.DateTimeField(blank=True, null=True, verbose_name=u'Срок выполнения')
    date_updated = models.DateTimeField(auto_now=True, verbose_name=u'Дата обновления')
    visible = models.CharField(max_length=10, choices=PUBLIC_STATUSES, default='public',
                               verbose_name=u'Доступность')
    community = models.ForeignKey(Community, related_name='tasks', blank=True, null=True,
                                         verbose_name=u'Опубликовать в сообществе')
    tags = TaggableManager(blank=True)
    comments = generic.GenericRelation(Comment)

    objects = TaskManager()

    class Meta:
        verbose_name = u'Задача'
        verbose_name_plural = u'Задачи'

    @property
    def is_past_due(self):
        if datetime.now() > self.date_due:
            return True
        return False

    def __unicode__(self):
        return self.title


class Checklist(models.Model):
    task = models.ForeignKey(Task, related_name='checklists', verbose_name=u'Задача')
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'Заголовок')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')

    def __unicode__(self):
        return self.title


class ChecklistItem(models.Model):
    checklist = models.ForeignKey(Checklist, related_name='items', verbose_name=u'Чеклист')
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'Заголовок')
    done = models.BooleanField(default=False, verbose_name=u'Сделано')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    date_done = models.DateTimeField(null=True, verbose_name=u'Дата выполнения')

    def __unicode__(self):
        return self.title
