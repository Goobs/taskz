# -*- coding: utf8 -*-
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail.admin import AdminImageMixin


from .models import *


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('full_name',)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        del self.fields['username']

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


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserCreationForm.Meta):
        model = User
        exclude = ('username',)

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        del self.fields['username']


class CustomUserAdmin(UserAdmin, AdminImageMixin):

    class ContactInline(admin.TabularInline):
        model = Contact
        extra = 0
        allow_add = True
        verbose_name = u'Контакт'
        verbose_name_plural = u'Контакты'

    inlines = (ContactInline, )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'dob', 'about', 'avatar', 'city')}),
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
    form = CustomUserChangeForm


admin.site.register(User, CustomUserAdmin)
