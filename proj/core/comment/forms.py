# -*- coding: utf-8 -*-

from proj.core.utils.crispymixin import *
from .models import *


class CommentForm(CrispyModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

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
