# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *


class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'recepient', 'read']

admin.site.register(Message, MessageAdmin)
