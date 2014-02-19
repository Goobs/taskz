# -*- coding: utf-8 -*-

from proj.core.utils.crispymixin import *
from django.contrib.auth.forms import *
from django.forms import widgets
from .models import *


class TaskEditForm(CrispyModelForm):
    class Meta:
        model = Task
        exclude = ['reporter']

    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'

        return Layout(
            Field('parent'),
            Field('assignee'),
            Field('project'),
            Field('milestone'),
            Field('status'),
            Field('priority'),
            Field('title'),
            Field('description'),
            Field('price'),
            Field('currency'),
            Field('date_due'),
            Field('visible'),
            Field('communities'),
            Field('tags'),
            Div(
                Div(
                    StrictButton(u'<i class="fa fa-save"></i> Сохранить',
                                 type='submit', name='save', value='1', css_class='btn-primary'),
                    css_class='form-group'
                ),
                css_class='col-md-9 col-md-offset-3'
            )
        )


class TaskCommentForm(CrispyModelForm):
    class Meta:
        model = TaskComment
        exclude = ['task', 'user', 'date']

    def get_layout(self, *args, **kwargs):
        self.helper.form_class = ''
        return Layout(
            Field('comment', rows=3),
            Div(
                StrictButton(u'<i class="fa fa-share"></i> Отправить',
                             type='submit', name='send', value='1', css_class='btn-primary'),
                css_class='form-group'
            )
        )


class TaskReplyForm(CrispyForm):
    task = forms.IntegerField(widget=widgets.HiddenInput)

    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'sr-only'
        self.helper.field_class = ''
        self.helper.form_method = 'post'
        return None


class TaskAssignForm(CrispyForm):
    user = forms.IntegerField(widget=widgets.HiddenInput)

    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'sr-only'
        self.helper.field_class = ''
        self.helper.form_method = 'post'
        return None
