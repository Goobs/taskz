# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *


class MessageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Message, MessageAdmin)
