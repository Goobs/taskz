# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q


class FeedManager(models.Manager):

    def user_feed(self, user):
        return self.filter(sender=user).order_by('-date')

    def people_feed(self, user):
        return self.filter(sender__in=user.friends.all(), community__isnull=True).order_by('-date')

    def user_community_feed(self, user):
        return self.filter(community__in=user.communities.all()).order_by('-date')

    def community_feed(self, community):
        return self.filter(community=community).order_by('-date')

    def common_feed(self, user):
        return self.filter(
            Q(sender__in=user.friends.all()) |
            Q(community__in=user.communities.all())
        ).order_by('-date')
