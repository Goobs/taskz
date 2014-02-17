# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import *
from django.views.generic.list import ListView
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from proj.core.models import User
from proj.core.message.models import Message
from .forms import *


class DialogListView(TemplateView):
    template_name = 'message/dialog_list.html'
    form = None
    recepient = None
    messages = None

    def get_context_data(self, **kwargs):
        if self.kwargs.get('user'):
            self.recepient = get_object_or_404(User, pk=self.kwargs.get('user'))

        if self.recepient and not self.form:
            self.form = ChatMessageForm(self.request.user, self.recepient)
            self.messages = Message.objects.dialog(self.request.user, self.recepient)[:20]
            for message in self.messages:
                if not message.read and message.recepient == self.request.user:
                    message.read = True
                    message.save()

        context = super(DialogListView, self).get_context_data(**kwargs)
        context['form'] = self.form
        context['chat'] = self.messages
        return context

    def post(self, request, **kwargs):
        if self.kwargs.get('user'):
            self.recepient = get_object_or_404(User, pk=self.kwargs.get('user'))
        if request.POST.get('send'):
            self.form = ChatMessageForm(self.request.user, self.recepient, request.POST)
            if self.form.is_valid():
                self.form.save()
                return redirect(request.META.get('HTTP_REFERER', None) or '/')
        return self.get(request, **kwargs)


class MessageModalView(TemplateView):
    template_name = 'message/message_modal.html'
    recepient = None
    form = None

    def get_context_data(self, **kwargs):
        self.recepient = get_object_or_404(User, pk=self.kwargs.get('user'))
        context = super(MessageModalView, self).get_context_data(**kwargs)
        if not self.form:
            self.form = ModalMessageForm(self.request.user, self.recepient)
        context['form'] = self.form
        return context

    def post(self, request, **kwargs):
        self.recepient = get_object_or_404(User, pk=self.kwargs.get('user'))
        if request.POST.get('send'):
            self.form = ModalMessageForm(request.user, self.recepient, request.POST)
            if self.form.is_valid():
                self.form.save()
                return redirect(request.META.get('HTTP_REFERER', None) or '/')
        return self.get(request, **kwargs)
