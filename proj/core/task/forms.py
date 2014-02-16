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
            Div(
                Div(
                    StrictButton(u'<i class="fa fa-save"></i> Сохранить',
                                 type='submit', name='save', value='1', css_class='btn-primary'),
                    css_class='form-group'
                ),
                css_class='col-md-9 col-md-offset-3'
            )
        )
