# -*- coding: utf-8 -*-

from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name=u'Название')

    class Meta:
        verbose_name = u'Страна'
        verbose_name_plural = u'Страны'

    def __unicode__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, related_name='cities', verbose_name=u'Страна')
    name = models.CharField(max_length=100, blank=True, verbose_name=u'Название')

    class Meta:
        verbose_name = u'Город'
        verbose_name_plural = u'Города'

    def __unicode__(self):
        return self.name
