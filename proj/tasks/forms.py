# -*- coding: UTF-8 -*-
from proj.core.utils.crispymixin import *
from django.contrib.auth.forms import *
from django.forms import widgets
from proj.core.feed.models import *
from proj.core.geo.models import *

from proj.core.models import *


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
        fields = ['full_name', 'city', 'dob', 'about', 'tags']
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
            'tags',
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


class UserAvatarForm(CrispyModelForm):
    class Meta:
        model = User
        fields = ['avatar']

    def get_layout(self, *args, **kwargs):
        return Layout(
            'avatar',
            Div(
                StrictButton(
                    u'<i class="fa fa-save"></i> Сохранить',
                    type='submit', name='save_avatar', value='1', css_class='btn btn-primary'
                ),
                css_class='col-md-9 col-md-offset-3'
            )
        )


class UserPasswordChangeForm(PasswordChangeForm, CrispyForm):
    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.form_class = 'form-horizontal'
        return Layout(
            'old_password',
            'new_password1',
            'new_password2',
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


class UserContactForm(CrispyModelForm):

    class Meta:
        model = Contact
        fields = ['id', 'type', 'value', 'public']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserContactForm, self).__init__(*args, **kwargs)

    def get_layout(self, *args, **kwargs):
        self.helper.form_tag = False
        return Layout(
            Div(
                Div(
                    InlineField('type'),
                    css_class='col-md-3'
                ),
                Div(
                    InlineField('value'),
                    css_class='col-md-5'
                ),
                Div(
                    InlineField('public'),
                    css_class='col-md-3'
                ),
                Div(
                    Div(
                        HTML('<a href="#" class="btn btn-link delete-form"><i class="fa fa-minus"></i></a>')
                            if not self.instance.id else
                            StrictButton('<i class="fa fa-minus text-danger"></i>',
                                         type='submit',
                                         name='delete_contact',
                                         value=self.instance.id,
                                         css_class='btn-link'),
                        css_class='form-group'
                    ),
                    css_class='col-md-1'
                ),
                css_class='row' if self.instance.id else 'row dynamic-form',
            ),

        )

    def save(self, *args, **kwargs):
        self.instance.user = self.user
        super(UserContactForm, self).save(*args, **kwargs)


class FollowUserForm(CrispyForm):
    user = forms.IntegerField(widget=forms.HiddenInput)

    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'sr-only'
        self.helper.field_class = ''
        self.helper.form_method = 'post'

        return None


class UserSearchForm(CrispyForm):
    query = forms.CharField(required=False, label=u'Поиск')
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False)
    friends = forms.CharField(required=False, widget=widgets.HiddenInput)

    def get_layout(self, *args, **kwargs):
        self.helper.form_class = 'form_inline'
        self.helper.form_method = 'get'
        self.helper.label_class = 'sr-only'
        return Layout(
            Div(
                Div(
                    FieldWithButtons(
                        InlineField('query', placeholder=u'Поиск'),
                        StrictButton(u'<i class="fa fa-search"></i> Поиск', type='submit', css_class='btn-default')
                    ),
                    css_class='col-md-6'
                ),
                Div(
                    InlineField('city'),
                    css_class='col-md-3'
                ),
                css_class='row'
            ),
            'friends',
        )
