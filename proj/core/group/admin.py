# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *


class GroupAdmin(admin.ModelAdmin):
    pass

admin.site.register(Group, GroupAdmin)
