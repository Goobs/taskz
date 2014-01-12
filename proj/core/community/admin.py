# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *


class CommunityAdmin(admin.ModelAdmin):
    pass

admin.site.register(Community, CommunityAdmin)
