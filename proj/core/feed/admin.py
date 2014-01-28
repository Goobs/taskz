# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from .models import *
from treeadmin.admin import TreeAdmin


class FeedAdmin(admin.ModelAdmin):
    list_display = ('sender', 'date')

admin.site.register(Feed, FeedAdmin)
