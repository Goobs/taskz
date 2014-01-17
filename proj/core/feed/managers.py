# -*- coding: utf-8 -*-
from django.db import models


class FeedManager(models.Manager):

    def user_feed(self, user):
        return self.filter(sender=user).order_by('-date')

    def people_feed(self):
        return self.filter(community__isnull=True).order_by('-date')

    def community_feed(self):
        return self.filter(community__isnull=False).order_by('-date')
