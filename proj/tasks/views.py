# -*- coding: utf-8 -*-
from django.views.generic import *
from django.views.generic.list import ListView
from django.shortcuts import redirect
from proj.core.feed.models import Feed
from proj.core.models import User


class FeedListView(ListView):
    model = Feed
    paginate_by = 20


class UserDetailView(DetailView):
    template_name = 'user/user_detail.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['userfeed'] = Feed.objects.user_feed(self.object)

        return context
