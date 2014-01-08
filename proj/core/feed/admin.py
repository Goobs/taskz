# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from .models import *
from treeadmin.admin import TreeAdmin


class FeedAdmin(admin.ModelAdmin):
    class CommentInline(admin.TabularInline):
        model = Comment
        extra = 0
        allow_add = False

    inlines = (CommentInline, )
    list_display = ['sender', 'title', 'date']

admin.site.register(Feed, FeedAdmin)


admin.site.register(Comment, TreeAdmin)
