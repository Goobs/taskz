# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from .views import *
from proj.core.utils.auth import *


urlpatterns = patterns(
    '',
    url(r'^$', login_required(FeedListView.as_view()), name='feed_list'),
    url(r'^(?P<pk>\d+)/?$', login_required(FeedDetailView.as_view()), name='feed_detail'),
)
