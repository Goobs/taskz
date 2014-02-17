# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from .views import *
from proj.core.utils.auth import *

urlpatterns = patterns(
    '',
    url(r'^$', unauthorized_only(LoginView.as_view())),

    url(r'^projects/', include('proj.core.project.urls')),
    url(r'^tasks/', include('proj.core.task.urls')),
    url(r'^messages/', include('proj.core.message.urls')),

    url(r'^feed/?$', login_required(FeedListView.as_view()), name='feed_list'),
    url(r'^feed/(?P<pk>\d+)/?$', login_required(FeedDetailView.as_view()), name='feed_detail'),

    url(r'^user/(?P<pk>\d+)/?$', UserDetailView.as_view(), name='user_detail'),
    url(r'^user/profile/?$', login_required(UserProfileView.as_view()), name='user_profile'),

    url(r'^accounts/login/$', unauthorized_only(LoginView.as_view()), name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    url(r'^communities/?$', login_required(CommunityListView.as_view()), name='community_list'),
    url(r'^communities/(?P<pk>\d+)/?$', login_required(CommunityDetailView.as_view()), name='community_detail'),

)
