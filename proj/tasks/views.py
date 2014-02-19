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
    model = User
    followform = None

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['userfeed'] = Feed.objects.user_feed(self.object)
        if not self.followform:
            self.followform = FollowUserForm(prefix='follow')
        context['followform'] = self.followform
        return context

    def post(self, request, **kwargs):

        if request.POST.get('follow-user'):
            self.followform = FollowUserForm(request.POST, prefix='follow')
            if self.followform.is_valid():
                user = User.objects.get(pk=self.followform.cleaned_data.get('user'))
                if not user in request.user.friends.all():
                    request.user.friends.add(user)
                else:
                    request.user.friends.remove(user)
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


class UserListView(ListView):
    model = User
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['searchform'] = UserSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        qs = User.objects.search(
            self.request.user,
            query=self.request.GET.get('query'),
            city=self.request.GET.get('city'),
            friends=self.request.GET.get('friends'),
        )
        return qs


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

