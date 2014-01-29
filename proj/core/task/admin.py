# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *


class TaskAdmin(admin.ModelAdmin):
    class TaskCommentInline(admin.TabularInline):
        model = TaskComment
        allow_add = True
        extra = 0
        verbose_name_plural = u'Комментарии'

    list_display = ('id', 'title', 'reporter', 'date_created', 'date_due', 'status')
    inlines = (TaskCommentInline,)

admin.site.register(Task, TaskAdmin)
