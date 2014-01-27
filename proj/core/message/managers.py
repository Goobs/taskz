# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q


class MessageManager(models.Manager):

    def dialog(self, user1, user2):
        return self.objects.filter(
            Q(sender=user1, recepient=user2) | Q(sender=user2, recepient=user2)
        ).order_by('date')
