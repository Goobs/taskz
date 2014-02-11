# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import *
from django.views.generic.list import ListView
from django.contrib.auth.views import *
from django.shortcuts import redirect, render
from django.contrib import messages
from django.forms.models import modelformset_factory
from django.utils.functional import curry
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
    profileform = None
    contactforms = modelformset_factory(Contact, form=UserContactForm, extra=1)

    def get_context_data(self, **kwargs):
        self.contactforms.form = staticmethod(curry(UserContactForm, user=self.request.user))
        context = super(UserProfileView, self).get_context_data(**kwargs)
        if not self.passwordform:
            self.passwordform = UserPasswordChangeForm(self.request.user, prefix='pass')
        if not self.profileform:
            self.profileform = EditProfileForm(instance=self.request.user, prefix='profile')
        context['profileform'] = self.profileform
        context['passwordform'] = self.passwordform
        context['contactforms'] = self.contactforms(queryset=self.request.user.contacts.all())
        return context

    def post(self, request, **kwargs):
        self.contactforms.form = staticmethod(curry(UserContactForm, user=request.user))
        if request.POST.get('profile'):
            self.profileform = EditProfileForm(request.POST, instance=request.user, prefix='profile')
            if self.profileform.is_valid():
                self.profileform.save()
                messages.success(request, u'Данные успешно изменены')
                return redirect('user_profile')
        if request.POST.get('pass_change'):
            self.passwordform = UserPasswordChangeForm(request.user, data=request.POST, prefix='pass')
            if self.passwordform.is_valid():
                self.passwordform.save()
                messages.success(request, u'Пароль изменен')
                return redirect('user_profile')
        if request.POST.get('save_contacts'):
            fs = self.contactforms(request.POST, queryset=self.request.user.contacts.all())
            if fs.is_valid:
                fs.save()
                messages.success(request, u'Контакты сохранены')
                return redirect('user_profile')
        if request.POST.get('delete_contact'):
            contact = Contact.objects.get(pk=request.POST.get('delete_contact'))
            if contact and contact.user == request.user:
                contact.delete()
                messages.success(request, u'Контакт удален')
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
