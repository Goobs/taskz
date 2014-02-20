# -*- coding: utf-8 -*-
from proj.core.utils.crispymixin import *
from .models import *


class FeedForm(CrispyModelForm):
    content = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Feed
        fields = ('content',)

    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'sr-only'
        self.helper.field_class = ''
        self.helper.form_method = 'post'

        return Layout(
            Div(
                Field('content', rows=2, placeholder=u'Напишите, что у вас нового'),
                css_class='col-md-12'
            ),
            StrictButton(u'<i class="fa fa-share"></i> Отправить', type='submit',
                         css_class='btn-primary', name='post', value='1'),
        )
