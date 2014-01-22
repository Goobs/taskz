# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns(
    '',
    (r'^$', IndexView.as_view(template_name='index.html')),
    url(r'^feed/?$', login_required(FeedListView.as_view()), name='feed_list'),
    url(r'^feed/(?P<pk>\d+)/?$', login_required(FeedDetailView.as_view()), name='feed_detail'),
    url(r'^user/(?P<pk>\d+)/?$', UserDetailView.as_view(), name='user_detail'),

    url(r'^accounts/login/$', LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
)
