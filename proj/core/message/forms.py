# -*- coding: utf-8 -*-
from proj.core.utils.crispymixin import *
from django.contrib.auth.forms import *
from django.forms import widgets

from .models import *


class ModalMessageForm(CrispyModelForm):
    class Meta:
        model = Message
        fields = ['message']
        widgets = {
            'message': widgets.Textarea()
        }

    def __init__(self, sender, recepient, *args, **kwargs):
        super(ModalMessageForm, self).__init__(*args, **kwargs)
        self.instance.sender = sender
        self.instance.recepient = recepient

    def get_layout(self, *args, **kwargs):
        self.helper.form_class = ''
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        return Layout(
            Field('message', rows=3),
            StrictButton(u'<i class="fa fa-share"></i> Отправить', type='submit',
                         css_class='btn-primary', name='send', value='1'),
        )


class ChatMessageForm(ModalMessageForm):
    def get_layout(self, *args, **kwargs):
        self.helper.form_class = ''
        self.helper.form_tag = True
        self.helper.label_class = 'sr-only'
        self.helper.form_method = 'post'
        return Layout(
            Field('message', rows=3, placeholder=u'Напишите сообщение'),
            StrictButton(u'<i class="fa fa-share"></i> Отправить', type='submit',
                         css_class='btn-primary', name='send', value='1'),
        )
