# -*- coding: utf8 -*-
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import *


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('full_name',)

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            self.Meta.model.objects.get(email=email)
        except self.Meta.model.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )


class CustomUserAdmin(UserAdmin):

    class ContactInline(admin.TabularInline):
        model = Contact
        extra = 0
        allow_add = True
        verbose_name = u'Контакт'
        verbose_name_plural = u'Контакты'

    inlines = (ContactInline, )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'about', 'avatar')}),
        (u'Социальные связи', {'fields': ('friends',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )

    list_display = ('email', 'full_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('full_name', 'email')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    add_form = CustomUserCreationForm


admin.site.register(User, CustomUserAdmin)
