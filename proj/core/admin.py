# -*- coding: utf8 -*-
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import admin


from .models import *


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('full_name',)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            self.Meta.model.objects.get(username=username)
        except self.Meta.model.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )


class CustomUserAdmin(UserAdmin):

    class ContactInline(admin.TabularInline):
        model = Contact
        extra = 0
        allow_add = True
        verbose_name = u'Контакт'
        verbose_name_plural = u'Контакты'

    inlines = (ContactInline, )

    custom_fieldset = (
        ((u'Персональные данные'), {'fields': ('full_name', )}),
    )

    fieldsets = UserAdmin.fieldsets + custom_fieldset
    add_fieldsets = UserAdmin.add_fieldsets + custom_fieldset

    add_form = CustomUserCreationForm


admin.site.register(User, CustomUserAdmin)
