# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from proj.core.models import User
from .managers import *


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    subject = generic.GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User, verbose_name=u'Пользователь')
    comment = models.TextField(max_length=1000, blank=True, null=True, verbose_name=u'Комментарий')
    date = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')

    objects = CommentManager()

    class Meta:
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'

    def __unicode__(self):
        return u'%s: %s' % (self.user, self.comment[:50])
