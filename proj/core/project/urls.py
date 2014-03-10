# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import *
from proj.core.utils.auth import *

urlpatterns = patterns(
    '',
    url(r'^$', login_required(ProjectListView.as_view()), name='project_list'),
    url(r'^(?P<pk>\d+)/?$', login_required(ProjectDetailView.as_view()), name='project_detail'),
    url(r'^edit/(?P<pk>\d+)?/?$', login_required(ProjectEditView.as_view()), name='project_edit'),
    url(r'^(?P<project>\d+)/milestone/(?P<pk>\d+)?/?$', login_required(MilestoneEditView.as_view()), name='milestone_edit'),
    url(r'^(?P<project>\d+)/milestones/?$', login_required(MilestoneListView.as_view()), name='milestone_list'),
)
