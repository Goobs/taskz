# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
    (r'^$', TemplateView.as_view(template_name='index.html')),
)