# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import *
from django.views.generic.list import ListView
from django.contrib.auth.views import *
from django.shortcuts import redirect, render
from django.forms.models import modelformset_factory
from .forms import *
from proj.core.feed.models import Feed
from proj.core.models import User


class IndexView(TemplateView):

    def get(self, request):
        if request.user.is_authenticated():
            return redirect(reverse('feed_list'))
        return HttpResponse(render(self.request, 'index.html'))


class FeedListView(ListView):
    model = Feed
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(FeedListView, self).get_context_data(**kwargs)
        context['getparam'] = self.request.GET.get('from')
        return context

    def get_queryset(self):
        param = self.request.GET.get('from')
        queryset = Feed.objects.all().order_by('-date')
        if param == 'communities':
            queryset = queryset.filter(community__isnull=False)
        elif param == 'people':
            queryset = queryset.filter(community__isnull=True)
        return queryset


class FeedDetailView(DetailView):
    model = Feed


class UserDetailView(DetailView):
    template_name = 'user/user_detail.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['userfeed'] = Feed.objects.user_feed(self.object)
        context['addform'] = FeedForm(form_method='post')
        return context

    def post(self, request, **kwargs):
        addform = FeedForm(request.POST)
        if addform.is_valid():
            feed = Feed(
                sender=request.user,
                content=addform.cleaned_data.get('content')
            )
            feed.save()
        return self.get(request, **kwargs)


class LoginView(TemplateView):
    template_name = 'accounts/login.html'
    form = LoginForm()

    def post(self, request):
        self.form = LoginForm(self.request.POST)
        self.form.is_valid()
        username = self.form.cleaned_data.get('username')
        password = self.form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(request.GET.get('next', '/'))
            else:
                self.form.errors['username'] = [u'Аккаунт неактивен']
        else:
            self.form.errors['__all__'] = [u'Неправильный логин и пароль']
        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context
