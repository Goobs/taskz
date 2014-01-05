# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', verbose_name=u'Пользователь')
    name = models.CharField(max_length=200, verbose_name=u'Имя')

    def __unicode__(self):
        return self.name


class Contact(models.Model):

    CONTACT_TYPES = (
        ('phone', u'Телефон'),
        ('email', u'E-mail'),
        ('skype', u'Skype'),
        ('icq', u'ICQ'),
        ('jabber', u'Jabber'),
        ('site', u'Site'),
    )
    profile = models.ForeignKey(Profile, verbose_name=u'Профиль')
    type = models.CharField(max_length=15, choices=CONTACT_TYPES, verbose_name=u'Тип')
    value = models.CharField(max_length=64, verbose_name=u'Значение', blank=True, null=True)
    public = models.BooleanField(default=False, verbose_name=u'Публичный')

    def __unicode__(self):
        return u'%s: %s' % (self.get_type_display(), self.value)
