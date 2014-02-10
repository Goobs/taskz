# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *


class CountryAdmin(admin.ModelAdmin):

    class CityInline(admin.TabularInline):
        model = City
        allow_add = True
        extra = 0

    inlines = (CityInline,)

admin.site.register(Country, CountryAdmin)


class CityAdmin(admin.ModelAdmin):
    pass

admin.site.register(City, CityAdmin)
