# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import *
from proj.core.utils.auth import *

urlpatterns = patterns(
    '',
    url(r'^(?P<user>\d+)?/?$', login_required(DialogListView.as_view()), name='dialog_list'),
    url(r'^modal/(?P<user>\d+)/?$', login_required(MessageModalView.as_view()), name='message_modal'),
)
