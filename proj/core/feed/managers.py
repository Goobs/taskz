# -*- coding: utf-8 -*-
from django.db import models


class FeedManager(models.Manager):

    def user_feed(self, user):
        return self.filter(sender=user)

    def people_feed(self):
        return self.filter(community__isnull=True)

    def community_feed(self):
        return self.filter(community__isnull=False)
