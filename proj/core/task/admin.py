# -*- coding: utf-8 -*-

from django.contrib import admin
from proj.core.comment.models import *
from .models import *


class TaskAdmin(admin.ModelAdmin):
    class CommentInline(generic.GenericTabularInline):
        model = Comment
        extra = 0
        allow_add = True

    list_display = ('id', 'title', 'reporter', 'date_created', 'date_due', 'status')
    inlines = (CommentInline,)

admin.site.register(Task, TaskAdmin)
