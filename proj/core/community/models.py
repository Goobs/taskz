# -*- coding: utf-8 -*-

from django.db import models
from proj.core.models import User


class Community(models.Model):
    users = models.ManyToManyField(User, related_name='communities', verbose_name=u'Пользователи')
    admin = models.ForeignKey(User, verbose_name=u'Администратор группы')
    name = models.CharField(max_length=250, verbose_name=u'Название')
    description = models.CharField(max_length=4000, verbose_name=u'Описание', null=True, blank=True)
    image = models.ImageField(upload_to='groups', verbose_name=u'Логотип', null=True, blank=True)

    class Meta:
        verbose_name = u'Сообщество'
        verbose_name_plural = u'Сообщества'

    def __unicode__(self):
        return self.name
