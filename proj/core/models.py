# -*- coding: utf8 -*-
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import re
from taggit.managers import TaggableManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlquote
from proj.core.geo.models import *


class UserManager(BaseUserManager):

    def _create_user(self, email, password, full_name,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, full_name=None, **extra_fields):
        return self._create_user(email, password, full_name, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password=None, full_name=None, **extra_fields):
        return self._create_user(email, password, full_name, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, db_index=True, blank=True)
    full_name = models.CharField(_('full name'), max_length=255, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    dob = models.DateField(blank=True, null=True, verbose_name=u'Дата рождения')
    avatar = models.ImageField(upload_to='users', null=True, blank=True, verbose_name=u'Аватар')
    about = models.TextField(blank=True, null=True, verbose_name=u'О себе')
    friends = models.ManyToManyField('self', symmetrical=False, blank=True, null=True, verbose_name=u'Друзья')

    city = models.ForeignKey(City, blank=True, null=True, related_name='users', verbose_name=u'Город')
    tags = TaggableManager(blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/user/%s/" % urlquote(self.pk)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """

        return self.full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.full_name.strip()

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return 'http://dummyimage.com/220x220'

    def __unicode__(self):
        return self.get_full_name()


class Contact(models.Model):

    CONTACT_TYPES = (
        ('phone', u'Телефон'),
        ('email', u'E-mail'),
        ('skype', u'Skype'),
        ('icq', u'ICQ'),
        ('jabber', u'Jabber'),
        ('site', u'Site'),
    )
    user = models.ForeignKey(User, related_name='contacts', verbose_name=u'Пользователь')
    type = models.CharField(max_length=15, choices=CONTACT_TYPES, default='phone', verbose_name=u'Тип')
    value = models.CharField(max_length=64, verbose_name=u'Значение', blank=True, null=True)
    public = models.BooleanField(default=False, verbose_name=u'Публичный')

    def __unicode__(self):
        return u'%s: %s' % (self.get_type_display(), self.value)


class Currency(models.Model):
    char_code = models.CharField(max_length=5, primary_key=True)
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=31)
    exchange_rate = models.FloatField(default=1)

    class Meta:
        verbose_name = u'Валюта'
        verbose_name_plural = u'Валюты'

    def __unicode__(self):
        return self.char_code
