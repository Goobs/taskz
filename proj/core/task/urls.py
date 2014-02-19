# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import *
from proj.core.utils.auth import *

urlpatterns = patterns(
    '',
    url(r'^$', login_required(TaskListView.as_view()), name='task_list'),
    url(r'^(?P<pk>\d+)/?$', login_required(TaskDetailView.as_view()), name='task_detail'),
    url(r'^edit/(?P<pk>\d+)?/?$', login_required(TaskEditView.as_view()), name='task_edit'),
)
