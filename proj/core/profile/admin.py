# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    """
    class UserInline(admin.TabularInline):
        model = User
        extra = 0
        allow_add = False

    inlines = (UserInline, )
    """
admin.site.register(Profile, ProfileAdmin)