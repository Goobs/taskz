# -*- coding: utf-8 -*-

from django.db import models
from proj.core.models import User
from .managers import *


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', verbose_name=u'Отправитель')
    recepient = models.ForeignKey(User, related_name='received_messages', verbose_name=u'Получатель')
    message = models.CharField(max_length=1024, verbose_name=u'Сообщение')
    date = models.DateTimeField(auto_now_add=True, verbose_name=u'Отправлено')
    read = models.BooleanField(default=False, verbose_name=u'Прочитано')

    objects = MessageManager()

    class Meta:
        verbose_name = u'Сообщение'
        verbose_name_plural = u'Сообщения'

    def __unicode__(self):
        return '%s -> %s %s' % (self.sender, self.recepient, self.date)
