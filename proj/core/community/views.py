# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import *
from django.views.generic.list import ListView
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .forms import *
from .models import *
from proj.core.feed.models import *
from proj.tasks.views import UserListView


class CommunityListView(ListView):
    model = Community
    paginate_by = 10

    def get_queryset(self):
        param = self.request.GET.get('filter')
        if param == 'following':
            queryset = Community.objects.filter(followers__in=[self.request.user.id])
        elif param == 'member':
            queryset = Community.objects.filter(users__user__id=self.request.user.id)
        else:
            queryset = Community.objects.all()
        return queryset


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
            if not community in request.user.follow_communities.all():
                request.user.follow_communities.add(community)
            else:
                request.user.follow_communities.remove(community)
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


class CommunityUsersView(UserListView):
    template_name = 'community/user_list.html'
    userform = None

    def get_queryset(self):
        qs = super(CommunityUsersView, self).get_queryset()
        if self.request.GET.get('show') == 'followers':
            return qs.filter(follow_communities__id=self.kwargs.get('pk'))
        return qs.filter(communities__id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(CommunityUsersView, self).get_context_data(**kwargs)
        context['object'] = get_object_or_404(Community, pk=self.kwargs.get('pk'))
        return context

    def post(self, request, **kwargs):
        if request.POST.get('user'):
            community = get_object_or_404(Community, pk=self.kwargs.get('pk'))
            if not community.admin == request.user:
                messages.error(request, u'Кулхацкер, да?')
                return redirect('community_users', pk=community.id)
            self.userform = CommunityUserForm(request.POST)
            if self.userform.is_valid:
                print self.userform
                user = get_object_or_404(User, pk=self.userform.cleaned_data.get('user'))
                if self.userform.cleaned_data.get('ban'):
                    community.followers.remove(user)
                    messages.success(request, u'Пользователь удален из сообщества')
                    return redirect('community_users', pk=community.id)
        return self.get(request, **kwargs)
