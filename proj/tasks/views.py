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
from proj.core.message.models import Message


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
        if param == 'communities':
            queryset = Feed.objects.community_feed(self.request.user)
        elif param == 'people':
            queryset = Feed.objects.people_feed(self.request.user)
        else:
            queryset = Feed.objects.common_feed(self.request.user)
        return queryset


class FeedDetailView(DetailView):
    model = Feed


class UserDetailView(DetailView):
    template_name = 'user/user_detail.html'
    model = User
    addform = FeedForm(prefix='add')
    followform = FollowUserForm(prefix='follow')

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['userfeed'] = Feed.objects.user_feed(self.object)
        context['addform'] = self.addform
        context['followform'] = self.followform
        return context

    def post(self, request, **kwargs):

        self.followform = FollowUserForm(request.POST, prefix='follow')
        if self.followform.is_valid():
            user = User.objects.get(pk=self.followform.cleaned_data.get('user'))
            request.user.friends.add(user)
            return self.get(request)

        self.addform = FeedForm(request.POST, prefix='add')
        if self.addform.is_valid() and request.POST.get('post'):
            feed = self.addform.instance
            feed.sender = request.user
            feed.content = self.addform.cleaned_data.get('content')
            feed.save()

        return self.get(request, **kwargs)


class LoginView(TemplateView):
    template_name = 'accounts/login.html'
    loginform = LoginForm(prefix='login')
    regform = RegistrationForm(prefix='reg')

    def post(self, request):
        email = None
        password = None
        self.loginform = LoginForm(self.request.POST, prefix='login')
        self.regform = RegistrationForm(self.request.POST, prefix='reg')

        if self.regform.is_valid():
            user = self.regform.instance
            email = user.email
            password = self.regform.cleaned_data.get('password')
            user.set_password(password)
            user.save()

        if self.loginform.is_valid():
            email = self.loginform.cleaned_data.get('email')
            password = self.loginform.cleaned_data.get('password')

        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect(request.GET.get('next', '/'))
            else:
                self.loginform.errors['email'] = [u'Аккаунт неактивен']
        else:
            self.loginform.errors['__all__'] = [u'Неправильный логин и пароль']
        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['loginform'] = self.loginform
        context['regform'] = self.regform
        return context


class MessagesListView(ListView):
    model = Message
    paginate_by = 20

