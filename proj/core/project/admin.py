# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *


class ProjectAdmin(admin.ModelAdmin):
    class MilestoneInline(admin.TabularInline):
        model = Milestone
        allow_add = True
        extra = 0
        verbose_name_plural = u'Вехи'

    list_display = ('id', 'title', 'reporter', 'date_created')
    inlines = (MilestoneInline,)

admin.site.register(Project, ProjectAdmin)
