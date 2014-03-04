# -*- coding: utf8 -*-
import hashlib
from django.core.mail import send_mail
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import re
from taggit.managers import TaggableManager
from sorl import thumbnail
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

    def search(self, user, **kwargs):
        qs = self
        query = kwargs.get('query')
        city = kwargs.get('city')
        friends = kwargs.get('friends')
        if query:
            qs = qs.filter(
                Q(full_name__icontains=query) |
                Q(email__icontains=query) |
                Q(tags__name__icontains=query)
            )
        if city:
            qs = qs.filter(city_id=city)
        if friends == 'followers':
            qs = qs.followers(user)
        elif friends == 'following':
            qs = qs.following(user)
        return qs.distinct()

    def followers(self, user):
        return self.filter(friends=user)

    def following(self, user):
        return self.filter(followers=user)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    full_name = models.CharField(_('full name'), max_length=255, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    dob = models.DateField(blank=True, null=True, verbose_name=u'Дата рождения')
    avatar = thumbnail.ImageField(upload_to='users', null=True, blank=True, verbose_name=u'Аватар')
    about = models.TextField(blank=True, null=True, verbose_name=u'О себе')
    friends = models.ManyToManyField('self', symmetrical=False, blank=True, null=True,
                                     related_name='followers', verbose_name=u'Друзья')

    city = models.ForeignKey(City, blank=True, null=True, related_name='users', verbose_name=u'Город')
    tags = TaggableManager(blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    abstract = False

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
    def gravatar(self):
        ghash = hashlib.md5(self.email.lower().strip()).hexdigest()
        return 'http://gravatar.com/avatar/%s?d=identicon' % ghash

    def avatar_url(self, width=80):
        if self.avatar:
            thumb = thumbnail.get_thumbnail(self.avatar, '%sx%s' % (width, width), crop='center', quality=99)
            return thumb.url
        return self.gravatar

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


def catch_ulogin_signal(*args, **kwargs):
    """
    Обновляет модель пользователя: исправляет username, имя и фамилию на
    полученные от провайдера.

    В реальной жизни следует иметь в виду, что username должен быть уникальным,
    а в социальной сети может быть много "тёзок" и, как следствие,
    возможно нарушение уникальности.

    """
    user=kwargs['user']
    json=kwargs['ulogin_data']

    if kwargs['registered']:
        user.full_name = json['first_name'] = ' ' + json['last_name']
        user.email = json['email']
        user.save()

from django_ulogin.models import ULoginUser
from django_ulogin.signals import assign

assign.connect(receiver=catch_ulogin_signal,
               sender=ULoginUser,
               dispatch_uid='customize.models')
