# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import *
from proj.core.utils.auth import *

urlpatterns = patterns(
    '',
    url(r'^$', unauthorized_only(LoginView.as_view())),
    url(r'^feed/?$', login_required(FeedListView.as_view()), name='feed_list'),
    url(r'^feed/(?P<pk>\d+)/?$', login_required(FeedDetailView.as_view()), name='feed_detail'),

    url(r'^user/(?P<pk>\d+)/?$', UserDetailView.as_view(), name='user_detail'),
    url(r'^user/profile/?$', login_required(UserProfileView.as_view()), name='user_profile'),

    url(r'^messages/?$', login_required(DialogListView.as_view()), name='dialog_list'),
    url(r'^messages/(?P<user>\d+)/?$', login_required(MessageListView.as_view()), name='message_list'),

    url(r'^accounts/login/$', unauthorized_only(LoginView.as_view()), name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    url(r'^projects/?$', login_required(ProjectListView.as_view()), name='project_list'),
    url(r'^projects/(?P<pk>\d+)/?$', login_required(ProjectDetailView.as_view()), name='project_detail'),

    url(r'^communities/?$', login_required(CommunityListView.as_view()), name='community_list'),
    url(r'^communities/(?P<pk>\d+)/?$', login_required(CommunityDetailView.as_view()), name='community_detail'),
)
