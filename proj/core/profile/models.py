# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=u'Пользователь')
    name = models.CharField(max_length=200, verbose_name=u'Имя')