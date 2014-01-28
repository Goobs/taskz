# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q


class MessageManager(models.Manager):

    def dialog(self, user1, user2):
        return self.filter(
            Q(sender=user1, recipient=user2) | Q(sender=user2, recipient=user1)
        ).order_by('date')


    def last(self, user):
        # TODO: Приделать Distinct
        return self.filter(Q(sender=user) | Q(recipient=user)).order_by('-date')
