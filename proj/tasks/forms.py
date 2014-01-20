# -*- coding: UTF-8 -*-
from proj.core.utils.crispymixin import *
from django.contrib.auth.forms import *
from django.forms import widgets
from proj.core.feed.models import *


class LoginForm(CrispyForm):
    username = forms.CharField(label=u'Логин')
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput())

    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        return Layout(
            Field('username'),
            'password',
            Div(
                Div(
                    StrictButton(u'<i class="fa fa-sign-in"></i> Войти', type='submit', css_class='btn-default'),
                    css_class='col-md-9 col-md-offset-3'
                ), css_class='form-group'
            )
        )


class FeedForm(CrispyModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'placeholder':u'Напишите, что у вас нового'}),)
    sender = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Feed
        fields = ('content', 'sender')

    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'sr-only'
        self.helper.field_class = ''

        return Layout(
            Div(
                Field('content'),
                css_class='col-md-12'
            ),
            StrictButton(u'<i class="fa fa-share-alt"></i> Отправить', type='submit', css_class='btn-primary'),
        )
