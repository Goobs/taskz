# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import *
from django.views.generic.list import ListView
from django.contrib.auth.views import *
from django.shortcuts import redirect, render
from django.contrib import messages
from django.forms.models import modelformset_factory
from .forms import *
from proj.core.feed.models import Feed
from proj.core.models import User
from proj.core.message.models import Message
from proj.core.project.models import Project
from proj.core.task.models import Task


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
            queryset = Feed.objects.user_community_feed(self.request.user)
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
    followform = FollowUserForm(prefix='follow')

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['userfeed'] = Feed.objects.user_feed(self.object)
        context['followform'] = self.followform
        return context

    def post(self, request, **kwargs):

        self.followform = FollowUserForm(request.POST, prefix='follow')
        if self.followform.is_valid():
            user = User.objects.get(pk=self.followform.cleaned_data.get('user'))
            request.user.friends.add(user)
            return self.get(request)

        return self.get(request, **kwargs)


class UserProfileView(TemplateView):
    template_name = 'accounts/profile_edit.html'
    passwordform = None

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        if not self.passwordform:
            self.passwordform = PasswordChangeForm(instance=self.request.user, prefix='pass')
        context['profileform'] = EditProfileForm(instance=self.request.user, prefix='profile')
        context['passwordform'] = self.passwordform
        return context

    def post(self, request, **kwargs):
        if request.POST.get('profile'):
            form = EditProfileForm(request.POST, instance=request.user, prefix='profile')
            if form.is_valid():
                form.save()
                messages.success(request, u'Данные успешно изменены')
                return redirect('user_profile')
        if request.POST.get('pass_change'):
            self.passwordform = EditProfileForm(request.POST, instance=request.user, prefix='pass')
            if self.passwordform.is_valid():
                #form.instance.set_password(form.cleaned_data.get('password_new'))
                #form.instance.save()
                messages.success(request, u'Пароль изменен')
                return redirect('user_profile')
        return self.get(request, **kwargs)


class LoginView(TemplateView):
    template_name = 'accounts/login.html'
    loginform = LoginForm(prefix='login')
    regform = RegistrationForm(prefix='reg')

    def post(self, request):
        email = None
        password = None

        if request.POST.get('signup'):
            self.regform = RegistrationForm(self.request.POST, prefix='reg')
            if self.regform.is_valid():
                user = self.regform.instance
                email = user.email
                password = self.regform.cleaned_data.get('password')
                user.set_password(password)
                user.save()

        if request.POST.get('login'):
            self.loginform = LoginForm(self.request.POST, prefix='login')
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


class DialogListView(ListView):
    template_name = 'message/dialog_list.html'
    model = Message
    paginate_by = 20

    def get_queryset(self):
        return Message.objects.last(self.request.user)


class MessageListView(ListView):
    model = Message

    def get_queryset(self):
        user2 = User.objects.get(pk=self.kwargs.get('user'))
        return Message.objects.dialog(self.request.user, user2)


class ProjectListView(ListView):
    model = Project
    paginate_by = 10

    def get_queryset(self):
        return Project.objects.filter(reporter=self.request.user)


class ProjectDetailView(DetailView):
    model = Project


class CommunityListView(ListView):
    model = Community
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.communities.all()


class CommunityDetailView(DetailView):
    model = Community

    def get_context_data(self, **kwargs):
        context = super(CommunityDetailView, self).get_context_data(**kwargs)
        context['userfeed'] = Feed.objects.community_feed(self.object)
        return context
