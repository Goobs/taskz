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
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'crispy_forms',
    'rest_framework',
    'mptt',
    'treeadmin',
    'taggit',
    'sorl.thumbnail',
    'reversion',
    'django_ulogin',

    'proj.cms.templates',
    'feincms',
    'feincms.module.page',
    'feincms.module.medialibrary',
    'proj.cms',

    #core
    'proj',
    'proj.core',
    'proj.core.community',
    'proj.core.feed',
    'proj.core.message',
    'proj.core.task',
    'proj.core.project',
    'proj.core.geo',
    'proj.core.comment',

    #app
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

SITE_ID = 1
FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'core', 'fixtures'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

AUTH_USER_MODEL = 'core.User'

FEINCMS_RICHTEXT_INIT_TEMPLATE = 'admin/content/richtext/init_tinymce4.html'
FEINCMS_RICHTEXT_INIT_CONTEXT = {
    'TINYMCE_JS_URL': STATIC_URL + 'cms/tinymce/tinymce.min.js',
}

from django.contrib.messages import constants
MESSAGE_TAGS = {
    constants.ERROR: 'danger',
}

ULOGIN_FIELDS = ['first_name', 'last_name', 'email']
ULOGIN_OPTIONAL = ['photo', 'bdate', 'city']
ULOGIN_PROVIDERS = ['vkontakte', 'facebook', 'mailru', 'google', 'odnoklassniki']
ULOGIN_HIDDEN = []
ULOGIN_DISPLAY = 'panel'
ULOGIN_CREATE_USER_CALLBACK = "proj.core.utils.ulogin.custom_user_create"
