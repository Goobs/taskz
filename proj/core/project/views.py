# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import *
from django.views.generic.list import ListView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Project
from .forms import *


class ProjectListView(ListView):
    model = Project
    paginate_by = 10

    def get_queryset(self):
        return Project.objects.filter(reporter=self.request.user)


class ProjectDetailView(DetailView):
    model = Project


class ProjectEditView(TemplateView):
    template_name = 'project/project_edit.html'
    object = None
    editform = None

    def get_context_data(self, **kwargs):
        context = super(ProjectEditView, self).get_context_data(**kwargs)
        if self.kwargs.get('pk'):
            self.object = Project.objects.get(pk=self.kwargs.get('pk'), reporter=self.request.user)
            if not self.object:
                return redirect('project_list')
        self.editform = ProjectEditForm(instance=self.object)
        context['form'] = self.editform
        return context

    def post(self, request, **kwargs):
        if self.kwargs.get('pk'):
            self.object = Project.objects.get(pk=self.kwargs.get('pk'), reporter=self.request.user)
        if request.POST.get('save'):
            self.editform = ProjectEditForm(request.POST, instance=self.object)
            if self.editform.is_valid():
                self.editform.instance.reporter = request.user
                self.editform.save()
                messages.success(request, u'Проект сохранен')
                redirect('project_edit', pk=self.editform.instance.id)
        return self.get(request, **kwargs)


class MilestoneListView(ListView):
    model = Milestone
    paginate_by = 10

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs.get('project'), reporter=self.request.user)
        return Milestone.objects.filter(
            project=project,
            project__reporter=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super(MilestoneListView, self).get_context_data(**kwargs)
        project = get_object_or_404(Project, pk=self.kwargs.get('project'), reporter=self.request.user)
        context['project'] = project
        return context


class MilestoneEditView(TemplateView):
    template_name = 'project/milestone_edit.html'
    object = None
    editform = None

    def get_context_data(self, **kwargs):
        context = super(MilestoneEditView, self).get_context_data(**kwargs)
        project = get_object_or_404(Project, pk=self.kwargs.get('project'), reporter=self.request.user)
        if self.kwargs.get('pk'):
            self.object = Milestone.objects.get(pk=self.kwargs.get('pk'),
                                                project__reporter=self.request.user,
                                                project=project)
            if not self.object:
                return redirect('project_list')
        self.editform = MilestoneEditForm(instance=self.object)
        context['project'] = project
        context['form'] = self.editform
        return context

    def post(self, request, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs.get('project'), reporter=self.request.user)
        if self.kwargs.get('pk'):
            self.object = Milestone.objects.get(pk=self.kwargs.get('pk'),
                                                project__reporter=self.request.user,
                                                project=project)
        if request.POST.get('save'):
            self.editform = MilestoneEditForm(request.POST, instance=self.object)
            if self.editform.is_valid():
                self.editform.instance.project = project
                self.editform.save()
                messages.success(request, u'Веха сохранена')
                redirect('milestone_edit', project=project.id, pk=self.editform.instance.id)
        return self.get(request, **kwargs)
