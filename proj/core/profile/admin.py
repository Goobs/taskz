# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):

    class ContactInline(admin.TabularInline):
        model = Contact
        extra = 0
        allow_add = True

    inlines = (ContactInline, )

admin.site.register(Profile, ProfileAdmin)
