# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.views.generic import *
from django.views.generic.list import ListView
from django.contrib.auth.views import *
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import *
from proj.core.models import User
from proj.core.task.models import Task
from proj.core.comment.models import *
from proj.core.comment.forms import *
from proj.core.utils.inlineeditview import InlineEditView


class TaskListView(ListView):
    model = Task
    paginate_by = 20
    form = None

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def get_queryset(self):
        self.form = TaskSearchForm(
            self.request.GET,
            projects=self.request.user.projects,
            milestones=self.request.user.milestones
        )
        self.form.is_valid()
        return Task.objects.search(
            project=self.form.cleaned_data.get('project'),
            milestone=self.form.cleaned_data.get('milestone'),
            status=self.request.GET.get('status'),
            query=self.request.GET.get('query'),
        )


class TaskDetailView(DetailView):
    model = Task
    commentform = None
    replyform = None
    assignform = None

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        self.commentform = CommentForm(prefix='comment')
        self.replyform = TaskReplyForm(prefix='reply')
        self.assignform = TaskAssignForm(prefix='assign')
        context['commentform'] = self.commentform
        context['replyform'] = self.replyform
        context['assignform'] = self.assignform
        return context

    def post(self, request, **kwargs):
        if request.POST.get('send'):
            self.commentform = CommentForm(request.POST, prefix='comment')
            self.commentform.instance.user = request.user
            self.commentform.instance.subject = get_object_or_404(Task, pk=self.kwargs.get('pk'))
            if self.commentform.is_valid():
                self.commentform.save()
                messages.success(request, u'Комментарий добавлен')
                return redirect('task_detail', pk=self.kwargs.get('pk'))
        if request.POST.get('reply-task'):
            self.replyform = TaskReplyForm(request.POST, prefix='reply')
            if self.replyform.is_valid():
                task = get_object_or_404(Task, pk=self.replyform.cleaned_data.get('task'))
                if request.user in task.repliers.all():
                    task.repliers.remove(request.user)
                    messages.success(request, u'Вы отазались от выполнения этой задачи')
                else:
                    task.repliers.add(request.user)
                    messages.success(request, u'Вы откликнулись на эту задачу')
                return redirect('task_detail', pk=self.kwargs.get('pk'))

        if request.POST.get('assign-user'):
            self.assignform = TaskAssignForm(request.POST, prefix='assign')
            if self.assignform.is_valid():
                user = get_object_or_404(User, pk=self.assignform.cleaned_data.get('user'))
                task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
                if user == task.assignee:
                    task.assignee = None
                    task.status = 'new'
                    messages.success(request, u'Вы сняли пользователя с этой задачи')
                else:
                    task.assignee = user
                    task.status = 'open'
                    messages.success(request, u'Вы назначили пользователя исполнителем на эту задачу')
                task.save()
                return redirect('task_detail', pk=self.kwargs.get('pk'))
        return self.get(request, **kwargs)


class TaskEditView(TemplateView):
    template_name = 'task/task_edit.html'
    form = None
    object = None

    def get_context_data(self, **kwargs):
        context = super(TaskEditView, self).get_context_data(**kwargs)
        if self.kwargs.get('pk'):
            self.object = get_object_or_404(Task, pk=self.kwargs.get('pk'), reporter=self.request.user)
        if not self.form:
            self.form = TaskEditForm(instance=self.object)
        context['form'] = self.form
        context['object'] = self.object
        return context

    def post(self, request, **kwargs):
        if self.kwargs.get('pk'):
            self.object = get_object_or_404(Task, pk=self.kwargs.get('pk'), reporter=request.user)
        if request.POST.get('save'):
            self.form = TaskEditForm(request.POST, instance=self.object)
            self.form.instance.reporter = request.user
            if self.form.is_valid():

                self.form.save()
                messages.success(request, u'Задача сохранена')
                return redirect('task_detail', pk=self.form.instance.pk)

        return self.get(request, **kwargs)


class TaskEditFieldView(InlineEditView):
    model = Task

