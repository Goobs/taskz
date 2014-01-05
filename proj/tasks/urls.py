# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns(
    '',
    (r'^$', TemplateView.as_view(template_name='index.html')),
    (r'^feed/?$', TemplateView.as_view(template_name='proto/feed.html')),
    (r'^user/?$', TemplateView.as_view(template_name='proto/user.html')),
)
