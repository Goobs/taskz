# -*- coding: utf-8 -*-
DEBUG = False
TEMPLATE_DEBUG = DEBUG

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-ru'

USE_I18N = True
USE_L10N = True
USE_TZ = False

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'crispy_forms',
    'mptt',
    'treeadmin',

    'proj',
    'proj.core',
    'proj.core.profile',
    'proj.core.group',
    'proj.core.feed',
    'proj.tasks',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'proj.urls'
WSGI_APPLICATION = 'proj.wsgi.application'

STATIC_URL = '/static/'

GRAPPELLI_ADMIN_TITLE = 'Goobs'
CRISPY_TEMPLATE_PACK = 'bootstrap3'

MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, '..', 'media'))
MEDIA_URL = '/media/'

#FIXTURE_DIRS = (
#    os.path.join(BASE_DIR, 'core', 'currency', 'fixtures'),
#)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

#AUTH_USER_MODEL = 'proj.core.User'
