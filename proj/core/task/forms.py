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
            Field('community'),
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


class TaskSearchForm(CrispyForm):
    query = forms.CharField(label=u'Поиск', required=False)
    project = forms.ModelChoiceField(queryset=None, required=False, empty_label=u'Все проекты')
    milestone = forms.ModelChoiceField(queryset=None, required=False, empty_label=u'Все вехи')
    status = forms.CharField(widget=widgets.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(TaskSearchForm, self).__init__(*args, **kwargs)
        self.fields['project'].queryset = kwargs.get('projects')
        self.fields['milestone'].queryset = kwargs.get('milestones')

    def get_layout(self, *args, **kwargs):
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'get'
        return Layout(
            InlineField('query'),
            InlineField('project'),
            InlineField('milestone'),
            'status',
            StrictButton(u'<i class="fa fa-search"></i> Поиск', css_class='btn-primary', type='submit')
        )
