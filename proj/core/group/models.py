# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    users = models.ManyToManyField(User, related_name='communities', verbose_name=u'Пользователи')
    admin = models.ForeignKey(User, verbose_name=u'Администратор группы')
    name = models.CharField(max_length=250, verbose_name=u'Название')
    description = models.CharField(max_length=4000, verbose_name=u'Описание', null=True, blank=True)
    image = models.ImageField(upload_to='groups', verbose_name=u'Логотип', null=True, blank=True)
