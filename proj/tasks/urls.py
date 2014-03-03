# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from .views import *
from proj.core.utils.auth import *

urlpatterns = patterns(
    '',
    url(r'^$', unauthorized_only(LoginView.as_view())),

    url(r'^projects/', include('proj.core.project.urls', app_name='project')),
    url(r'^tasks/', include('proj.core.task.urls', app_name='task')),
    url(r'^messages/', include('proj.core.message.urls', app_name='message')),
    url(r'^community/', include('proj.core.community.urls', app_name='community')),
    url(r'^feed/', include('proj.core.feed.urls', app_name='feed')),

    url(r'^user/(?P<pk>\d+)/?$', UserDetailView.as_view(), name='user_detail'),
    url(r'^user/profile/?$', login_required(UserProfileView.as_view()), name='user_profile'),
    url(r'^users/?$', login_required(UserListView.as_view()), name='user_list'),


    url(r'^accounts/login/$', unauthorized_only(LoginView.as_view()), name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    url(r'^blog/', include('proj.cms.urls')),


)
