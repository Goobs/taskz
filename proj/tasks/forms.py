# -*- coding: UTF-8 -*-
from proj.core.utils.crispymixin import *
from django.contrib.auth.forms import *
from django.forms import widgets
from proj.core.feed.models import *
from proj.core.geo.models import *


class LoginForm(CrispyForm):
    email = forms.EmailField(label=u'Email')
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput)

    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'sr-only'
        self.helper.field_class = ''
        self.helper.form_class = ''
        return Layout(
            Field('email', placeholder=u'Логин'),
            Div(
                Div(
                    Field('password', placeholder=u'Пароль'),
                    css_class='col-md-8'
                ),
                Div(
                    StrictButton(u'<i class="fa fa-sign-in"></i> Войти', type='submit',
                                 css_class='btn-primary btn-block', name='login', value='on'),
                    css_class='col-md-4'
                ),
                css_class='row'
            ),
        )


class RegistrationForm(CrispyModelForm):
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['full_name', 'email']

    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'sr-only'
        self.helper.field_class = ''
        self.helper.form_class = ''
        return Layout(
            Field('full_name', placeholder=u'Ваше имя'),
            Field('email', placeholder=u'E-mail'),
            Field('password', placeholder=u'Пароль'),
            StrictButton(u'Регистрация', type='submit', css_class='btn-default pull-right',
                         name='signup', value='on'),
            Div(css_class='clearfix')
        )


class EditProfileForm(CrispyModelForm):
    #city = forms.ModelChoiceField(queryset=City.objects.all(), required=False, widget=widgets.ChoiceInput())

    class Meta:
        model = User
        fields = ['full_name', 'city', 'dob', 'about']
        labels = {
            'full_name': u'Ваше имя'
        }

    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.form_class = 'form-horizontal'
        return Layout(
            'full_name',
            'dob',
            'city',
            Field('about', rows=3),
            Div(
                Div(
                    StrictButton(
                        u'<i class="fa fa-save"></i> Сохранить',
                        type='submit', name='profile', value='1', css_class='btn btn-primary'
                    ),
                    css_class='col-md-9 col-md-offset-3'
                ),
                css_class='form-group'
            )
        )


class PasswordChangeForm(CrispyModelForm):
    passwd = forms.CharField(label=u'Текущий пароль', widget=widgets.PasswordInput)
    password_new = forms.CharField(label=u'Новый пароль', widget=widgets.PasswordInput)
    password_retry = forms.CharField(label=u'Повторите пароль', widget=widgets.PasswordInput)

    class Meta:
        model = User

    def clean_passwd(self):
        passwd = self.data['passwd']
        if not self.instance.check_password(passwd):
            msg = u'Неправильный пароль'
            raise forms.ValidationError(msg)
        return passwd

    def clean_password_retry(self):
        passwd = self.cleaned_data['password_new']
        passwd_retry = self.cleaned_data['password_retry']
        if passwd != passwd_retry:
            msg = u'Пароли не совпадают!'
            raise forms.ValidationError(msg)
        return passwd_retry

    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.form_class = 'form-horizontal'
        return Layout(
            'passwd',
            'password_new',
            'password_retry',
            Div(
                Div(
                    StrictButton(
                        u'<i class="fa fa-save"></i> Сменить пароль',
                        type='submit', name='pass_change', value='1', css_class='btn btn-primary'
                    ),
                    css_class='col-md-9 col-md-offset-3'
                ),
                css_class='form-group'
            )
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


