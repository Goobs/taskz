# -*- coding: utf-8 -*-
from proj.core.utils.crispymixin import *
from django.forms import widgets
from .models import *


class FollowCommunityForm(CrispyForm):
    community = forms.IntegerField(widget=forms.HiddenInput)

    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'sr-only'
        self.helper.field_class = ''
        self.helper.form_method = 'post'

        return None


class CommunityForm(CrispyModelForm):
    class Meta:
        model = Community
        fields = ['name', 'image', 'description', 'tags']
        widgets = {
            'description': widgets.Textarea()
        }

    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-6'
        return Layout(
            'name',
            'image',
            'description',
            'tags',
            Div(
                Div(
                    StrictButton(u'<i class="fa fa-save"></i> Сохранить',
                                 type='submit', name='save', value='1', css_class='btn-primary'),
                    css_class='form-group'
                ),
                css_class='col-md-6 col-md-offset-3'
            )
        )
