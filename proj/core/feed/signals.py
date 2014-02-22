# -*- coding: utf-8 -*-
from django.db.models.signals import *
from django.dispatch import receiver
from django.template import Context
from django.template.loader import get_template
from .models import *
from proj.core.project.models import *
from proj.core.task.models import *


@receiver(post_save, sender=Project)
def project_saved(sender, instance, created, **kwargs):
    if instance.visible != 'private':
        if created:
            template_name = 'project_created.html'
        else:
            template_name = 'project_updated.html'
        template = get_template(template_name)
        content = template.render(Context({'project': instance}))
        feed = Feed(
            sender=instance.reporter,
            community=None,
            title=instance.title,
            content=content
        )
        feed.save()


@receiver(post_save, sender=Task)
def task_saved(sender, instance, created, **kwargs):
    if instance.visible != 'private':
        if created:
            template_name = 'task_created.html'
        else:
            template_name = 'task_updated.html'
        template = get_template(template_name)
        content = template.render(Context({'task': instance}))
        community = None
        if instance.community:
            community = instance.community
        feed = Feed(
            sender=instance.reporter,
            community=community,
            title=instance.title,
            content=content
        )
        feed.save()


@receiver(m2m_changed, sender=User.friends.through)
def user_follow(sender, instance, **kwargs):
    if kwargs.get('action') == 'post_add':
        template_name = 'user_follow.html'
    elif kwargs.get('action') == 'post_remove':
        template_name = 'user_unfollow.html'
    else:
        return
    template = get_template(template_name)
    user1 = instance
    user2 = User.objects.get(pk__in=kwargs.get('pk_set'))
    content = template.render(Context({'user1': user1, 'user2': user2}))
    feed = Feed(
        sender=user1,
        community=None,
        title=u'Подписка',
        content=content
    )
    feed.save()

    if kwargs.get('action') == 'post_remove':

        feed = Feed(
            sender=user2,
            community=None,
            title=u'Отписка',
            content=content
        )
        feed.save()


@receiver(m2m_changed, sender=Community.users.through)
def community_follow(sender, instance, **kwargs):
    if kwargs.get('action') == 'post_add':
        template_name = 'community_follow.html'
    elif kwargs.get('action') == 'post_remove':
        template_name = 'community_unfollow.html'
    else:
        return
    template = get_template(template_name)
    user1 = instance
    community = Community.objects.get(pk__in=kwargs.get('pk_set'))
    content = template.render(Context({'user1': user1, 'community': community}))
    feed = Feed(
        sender=user1,
        community=None,
        title=u'Подписка',
        content=content
    )
    feed.save()

    if kwargs.get('action') == 'post_remove':

        feed = Feed(
            sender=user1,
            community=None,
            title=u'Отписка',
            content=content
        )
        feed.save()


