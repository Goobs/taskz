# -*- coding: utf-8 -*-

from django.db import models
from proj.core.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', verbose_name=u'Отправитель')
    recipient = models.ForeignKey(User, related_name='received_messages', verbose_name=u'Получатель')
    message = models.CharField(max_length=1024, verbose_name=u'Сообщение')
    date = models.DateTimeField(auto_now_add=True, verbose_name=u'Отправлено')
    read = models.BooleanField(default=False, verbose_name=u'Прочитано')

    class Meta:
        verbose_name = u'Сообщение'
        verbose_name_plural = u'Сообщения'

    def __unicode__(self):
        return self.name
