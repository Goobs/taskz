# -*- coding: utf-8 -*-

from django.db.models import Manager, Q


class CommunityManager(Manager):

    def search(self, request, query=None, filter_param=None):
        qs = self
        if query:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(tags__name__icontains=query)
            )
        if filter_param == 'following':
            qs = qs.filter(followers__id=request.user.id)
        if filter_param == 'member':
            qs = qs.filter(users__id=request.user.id)
        return qs
