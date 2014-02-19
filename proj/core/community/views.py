# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import *
from django.views.generic.list import ListView
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .forms import *
from .models import *
from proj.core.feed.models import *


class CommunityListView(ListView):
    model = Community
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.communities.all()


class CommunityDetailView(DetailView):
    model = Community
    followform = FollowCommunityForm(prefix='follow')

    def get_context_data(self, **kwargs):
        context = super(CommunityDetailView, self).get_context_data(**kwargs)
        context['userfeed'] = Feed.objects.community_feed(self.object)
        context['followform'] = self.followform
        return context

    def post(self, request, **kwargs):

        self.followform = FollowCommunityForm(request.POST, prefix='follow')
        if self.followform.is_valid():
            community = Community.objects.get(pk=self.followform.cleaned_data.get('community'))
            if not community in request.user.communities.all():
                request.user.communities.add(community)
            else:
                request.user.communities.remove(community)
            return self.get(request)

        return self.get(request, **kwargs)


class CommunityEditView(TemplateView):
    template_name = 'community/community_edit.html'
    form = None
    community = None

    def get_context_data(self, **kwargs):
        context = super(CommunityEditView, self).get_context_data(**kwargs)
        if self.kwargs.get('pk'):
            self.community = get_object_or_404(Community, pk=self.kwargs.get('pk'), admin=self.request.user)
        if not self.form:
            self.form = CommunityForm(instance=self.community)
        context['form'] = self.form
        return context

    def post(self, request, **kwargs):
        if self.kwargs.get('pk'):
            self.community = get_object_or_404(Community, pk=self.kwargs.get('pk'), admin=request.user)
        if request.POST.get('save'):
            self.form = CommunityForm(request.POST, request.FILES, instance=self.community)
            self.form.instance.admin = request.user
            if self.form.is_valid():
                self.form.save()
                self.form.instance.users.add(request.user)
                messages.success(request, u'Изменения сохранены')
                return redirect('community_detail', self.form.instance.id)

        return self.get(request, **kwargs)
