# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.generic import *
from django.views.generic.list import ListView
from django.contrib.auth.views import *
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import *
from proj.core.models import User
from proj.core.task.models import Task


class TaskListView(ListView):
    model = Task
    paginate_by = 20


class TaskDetailView(DetailView):
    model = Task


class TaskEditView(TemplateView):
    template_name = 'task/task_edit.html'
    form = None
    object = None

    def get_context_data(self, **kwargs):
        context = super(TaskEditView, self).get_context_data(**kwargs)
        if self.kwargs.get('pk'):
            self.object = Task.objects.get(pk=self.kwargs.get('pk'), reporter=self.request.user)
        if not self.form:
            self.form = TaskEditForm(instance=self.object)
        context['form'] = self.form
        return context

    def post(self, request, **kwargs):
        if self.kwargs.get('pk'):
            self.object = Task.objects.get(pk=self.kwargs.get('pk'), reporter=request.user)
        if request.POST.get('save'):
            self.form = TaskEditForm(request.POST, instance=self.object)
            self.form.instance.reporter = request.user
            if self.form.is_valid():

                self.form.save()
                messages.success(request, u'Задача сохранена')
                return redirect('task_detail', pk=self.object.id)

        return self.get(request, **kwargs)
