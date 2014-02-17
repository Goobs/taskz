# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q

from proj.core.models import User


class MessageManager(models.Manager):

    def dialog(self, user1, user2):
        return self.filter(
            Q(sender=user1, recepient=user2) | Q(sender=user2, recepient=user1)
        ).order_by('date')

    def last(self, user):
        users = User.objects.filter(
            (Q(sent_messages__sender=user) | Q(sent_messages__recepient=user)) & ~Q(pk=user.id)
        ).prefetch_related('sent_messages', 'received_messages').distinct()
        msg_ids = []
        for user in users:
            sent = user.sent_messages.latest('date')
            rcvd = user.received_messages.latest('date')
            if sent.date > rcvd.date:
                msg_ids.append(sent.id)
            else:
                msg_ids.append(rcvd.id)
        return self.filter(pk__in=msg_ids).order_by('-date')
