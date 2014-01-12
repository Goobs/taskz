# -*- coding: utf8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'Полное имя')


class Contact(models.Model):

    CONTACT_TYPES = (
        ('phone', u'Телефон'),
        ('email', u'E-mail'),
        ('skype', u'Skype'),
        ('icq', u'ICQ'),
        ('jabber', u'Jabber'),
        ('site', u'Site'),
    )
    user = models.ForeignKey(User, verbose_name=u'Профиль')
    type = models.CharField(max_length=15, choices=CONTACT_TYPES, verbose_name=u'Тип')
    value = models.CharField(max_length=64, verbose_name=u'Значение', blank=True, null=True)
    public = models.BooleanField(default=False, verbose_name=u'Публичный')

    def __unicode__(self):
        return u'%s: %s' % (self.get_type_display(), self.value)
