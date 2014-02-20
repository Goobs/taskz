# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import *
from proj.core.utils.auth import *

urlpatterns = patterns(
    '',
    url(r'^$', login_required(CommunityListView.as_view()), name='community_list'),
    url(r'^(?P<pk>\d+)/?$', login_required(CommunityDetailView.as_view()), name='community_detail'),
    url(r'^edit/?$', login_required(CommunityEditView.as_view()), name='community_edit'),
    url(r'^(?P<pk>\d+)?/edit/?$', login_required(CommunityEditView.as_view()), name='community_edit'),
    url(r'^(?P<pk>\d+)/users/?$', login_required(CommunityUsersView.as_view()), name='community_users'),
)
