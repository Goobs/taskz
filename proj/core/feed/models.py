# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from proj.core.models import User
import mptt


class Feed(models.Model):

    sender = models.ForeignKey(User, verbose_name=u'Отправитель')
    title = models.CharField(max_length=255, blank=True, null=True, default='', verbose_name=u'Заголовок')
    content = models.TextField(blank=True, null=True, default='', verbose_name=u'Содержание')
    date = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    feed = models.ForeignKey(Feed, related_name='comments', verbose_name=u'Пост')
    parent = models.ForeignKey('self', related_name='children',  blank=True, null=True, verbose_name=u'Родитель')
    sender = models.ForeignKey(User, verbose_name=u'Отправитель')
    comment = models.TextField(max_length=4096, default='', verbose_name=u'Комментарий')
    date = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')

    class MPTTMeta:
        order_insertion_by = ['date']

    def __unicode__(self):
        return '%s: %s' % (self.sender, self.comment)

mptt.register(Comment,)
