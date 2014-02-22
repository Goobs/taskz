# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from proj.core.models import User
from proj.core.community.models import Community
from proj.core.comment.models import Comment
from taggit.managers import TaggableManager
import mptt
from .managers import *



class Feed(models.Model):

    sender = models.ForeignKey(User, verbose_name=u'Отправитель')
    community = models.ForeignKey(Community, blank=True, null=True, verbose_name=u'Сообщество')
    title = models.CharField(max_length=255, blank=True, null=True, default='', verbose_name=u'Заголовок')
    content = models.TextField(blank=True, null=True, default='', verbose_name=u'Содержание')
    date = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    tags = TaggableManager(blank=True)
    comments = generic.GenericRelation(Comment)

    objects = FeedManager()

    def __unicode__(self):
        return self.content[:20]
