# -*- coding: utf-8 -*-

from proj.core.utils.crispymixin import *
from django.contrib.auth.forms import *
from django.forms import widgets
from .models import *


class ProjectEditForm(CrispyModelForm):

    class Meta:
        model = Project
        exclude = ['reporter']

    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'

        return Layout(
            Field('title'),
            Field('description', rows='7'),
            Field('status'),
            Field('visible'),
            Field('date_due'),
            Div(
                Div(
                    StrictButton(u'<i class="fa fa-save"></i> Сохранить',
                                 type='submit', name='save', value='1', css_class='btn-primary'),
                    css_class='form-group'
                ),
                css_class='col-md-9 col-md-offset-3'
            )
        )
