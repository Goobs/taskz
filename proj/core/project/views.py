# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import *
from django.views.generic.list import ListView
from django.shortcuts import redirect
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
            print self.object
            self.editform = ProjectEditForm(request.POST, instance=self.object)
            if self.editform.is_valid():

                self.editform.instance.reporter = request.user
                self.editform.save()
                messages.success(request, u'Проект сохранен')
                redirect('project_edit', **self.kwargs)
            print self.editform.errors
        return self.get(request, **kwargs)
