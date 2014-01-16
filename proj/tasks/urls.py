# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns(
    '',
    (r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^feed/?$', FeedListView.as_view(), name='feed_list'),
    url(r'^user/(?P<pk>\d+)/$', UserDetailView.as_view(), name='user_detail'),
)
