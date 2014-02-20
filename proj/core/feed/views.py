# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import *
from django.views.generic.list import ListView
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import *
from .models import *


class FeedListView(ListView):
    model = Feed
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(FeedListView, self).get_context_data(**kwargs)
        context['getparam'] = self.request.GET.get('from')
        return context

    def get_queryset(self):
        param = self.request.GET.get('from')
        if param == 'communities':
            queryset = Feed.objects.user_community_feed(self.request.user)
        elif param == 'people':
            queryset = Feed.objects.people_feed(self.request.user)
        else:
            queryset = Feed.objects.common_feed(self.request.user)
        return queryset


class FeedDetailView(DetailView):
    model = Feed
