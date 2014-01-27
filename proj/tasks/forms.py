# -*- coding: UTF-8 -*-
from proj.core.utils.crispymixin import *
from django.contrib.auth.forms import *
from django.forms import widgets
from proj.core.feed.models import *


class LoginForm(CrispyForm):
    username = forms.CharField(label=u'Логин')
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput)

    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'sr-only'
        self.helper.field_class = ''
        self.helper.form_class = ''
        return Layout(
            Field('username', placeholder=u'Логин'),
            Div(
                Div(
                    Field('password', placeholder=u'Пароль'),
                    css_class='col-md-8'
                ),
                Div(
                    StrictButton(u'<i class="fa fa-sign-in"></i> Войти', type='submit',
                                 css_class='btn-primary btn-block'),
                    css_class='col-md-4'
                ),
                css_class='row'
            ),
        )


class RegistrationForm(CrispyModelForm):
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email']

    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'sr-only'
        self.helper.field_class = ''
        self.helper.form_class = ''
        return Layout(
            Field('username', placeholder=u'Логин'),
            Field('full_name', placeholder=u'Ваше имя'),
            Field('email', placeholder=u'E-mail'),
            Field('password', placeholder=u'Пароль'),
            StrictButton(u'Регистрация', type='submit', css_class='btn-default pull-right'),
            Div(css_class='clearfix')
        )


class FeedForm(CrispyModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'placeholder': u'Напишите, что у вас нового'}),)

    class Meta:
        model = Feed
        fields = ('content',)

    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'sr-only'
        self.helper.field_class = ''
        self.helper.form_method = 'post'

        return Layout(
            Div(
                Field('content'),
                css_class='col-md-12'
            ),
            StrictButton(u'<i class="fa fa-share"></i> Отправить', type='submit',
                         css_class='btn-primary', name='post', value='1'),
        )


class FollowUserForm(CrispyForm):
    user = forms.IntegerField(widget=forms.HiddenInput)

    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'sr-only'
        self.helper.field_class = ''
        self.helper.form_method = 'post'

        return Layout(
            'user',
            StrictButton(u'<i class="fa fa-star"></i> Подписаться', type='submit',
                         css_class='btn-primary')
        )
